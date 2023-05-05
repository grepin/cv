import functools
import logging
import time
from json import loads

import pika
from core.config import settings
from executor.tasks.cancel_payment import cancel_payment
from executor.tasks.check_payment import check_payment
from executor.tasks.repay import repay
from pika.exchange_type import ExchangeType

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
LOGGER = logging.getLogger(__name__)


class Consumer:
    EXCHANGE = ''
    EXCHANGE_TYPE = ExchangeType.direct
    QUEUE = 'payments'
    ROUTING_KEY = 'payments'

    def __init__(self, user: str, password: str, host: str, exchange: str, queue: str, routing_key: str):
        self.EXCHANGE = exchange
        self.ROUTING_KEY = routing_key
        self.QUEUE = queue

        self.should_reconnect = False
        self.was_consuming = False

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = 'amqp://{0}:{1}@{2}/%2F'.format(user, password, host)
        self._consuming = False
        self._prefetch_count = 1

    def connect(self):
        LOGGER.info('Connecting to %s', self._url)
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            LOGGER.info('Connection is closing or already closed')
        else:
            LOGGER.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        LOGGER.error('Connection open failed: %s', err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        LOGGER.info('Binding %s to %s with %s', self.EXCHANGE, self.QUEUE,
                    self.ROUTING_KEY)
        cb = functools.partial(self.on_bindok)
        self._channel.queue_bind(
            self.QUEUE,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def add_on_channel_close_callback(self):
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        LOGGER.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def on_bindok(self, _unused_frame):
        LOGGER.info('Queue bound: %s', self.QUEUE)
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        LOGGER.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r', method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        try:
            json = loads(body)
            if 'subscription_id' not in json:
                raise AssertionError('no subscription_id in doc')
            if 'provider' not in json:
                raise AssertionError('no provider in doc')
            if 'from' not in properties.headers:
                raise AssertionError('no from in headers: {0}'.format(json))
            if properties.headers['from'] not in ['client-admin', 'callback', 'client-cancel', 'client-repay']:
                raise AssertionError('no valid from in headers: {0}'.format(json))
            if properties.headers['from'] == 'callback':
                task_id = "{0}.{1}".format(json['subscription_id'], properties.headers['from'])
                check_payment.apply_async(
                    args=[json],
                    task_id=task_id,
                )
            if properties.headers['from'] == 'client-cancel':
                task_id = "{0}.{1}".format(json['subscription_id'], properties.headers['from'])
                cancel_payment.apply_async(
                    args=[json],
                    task_id=task_id,
                )
            if properties.headers['from'] == 'client-repay':
                task_id = "{0}.{1}".format(json['subscription_id'], properties.headers['from'])
                repay.apply_async(
                    args=[json],
                    task_id=task_id,
                )
            self._channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
        except Exception as e:
            LOGGER.info('{0}: {1}'.format(type(e).__name__, e))
            self._channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def stop_consuming(self):
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        LOGGER.info(
            'RabbitMQ acknowledged the cancellation of the consumer: %s',
            userdata)
        self.close_channel()

    def close_channel(self):
        LOGGER.info('Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            LOGGER.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            LOGGER.info('Stopped')


class ReconnectingConsumer(object):

    def __init__(self, RMQ_USER, RMQ_PASSWORD, RMQ_HOST, RMQ_PAYMENTS_EXCHANGE,
                 RMQ_PAYMENTS_QUEUE, RMQ_PAYMENTS_ROUTING_KEY):
        self.RMQ_USER = RMQ_USER
        self.RMQ_PASSWORD = RMQ_PASSWORD
        self.RMQ_HOST = RMQ_HOST
        self.RMQ_PAYMENTS_EXCHANGE = RMQ_PAYMENTS_EXCHANGE
        self.RMQ_PAYMENTS_QUEUE = RMQ_PAYMENTS_QUEUE
        self.RMQ_PAYMENTS_ROUTING_KEY = RMQ_PAYMENTS_ROUTING_KEY
        self._reconnect_delay = 0
        self._consumer = Consumer(
            self.RMQ_USER,
            self.RMQ_PASSWORD,
            self.RMQ_HOST,
            self.RMQ_PAYMENTS_EXCHANGE,
            self.RMQ_PAYMENTS_QUEUE,
            self.RMQ_PAYMENTS_ROUTING_KEY)
        self._amqp_url = self._consumer._url

    def run(self):
        while True:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self._consumer.should_reconnect:
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            LOGGER.info('Reconnecting after %d seconds', reconnect_delay)
            time.sleep(reconnect_delay)
            self._consumer = Consumer(
                self.RMQ_USER,
                self.RMQ_PASSWORD,
                self.RMQ_HOST,
                self.RMQ_PAYMENTS_EXCHANGE,
                self.RMQ_PAYMENTS_QUEUE,
                self.RMQ_PAYMENTS_ROUTING_KEY
            )

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    consumer = ReconnectingConsumer(
        settings.RMQ_USER,
        settings.RMQ_PASSWORD,
        settings.RMQ_HOST,
        settings.RMQ_PAYMENTS_EXCHANGE,
        settings.RMQ_PAYMENTS_QUEUE,
        settings.RMQ_PAYMENTS_ROUTING_KEY)
    consumer.run()


if __name__ == '__main__':
    main()
