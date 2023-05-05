from typing import Optional

import pika
from pika.exceptions import AMQPError


class RabbitMQ:
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        exchange: str,
        routing_key: str,
    ):
        self.credentials = pika.PlainCredentials(user, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            virtual_host='/',
            credentials=self.credentials,
            blocked_connection_timeout=1,
            heartbeat=65535
        )
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = None
        self.channel = None

    def _channel(self):
        if self.connection is None or not self.connection.is_open():
            self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def start(self):
        self._channel()

    async def publish(self, message: str, headers: dict = {}):
        try:
            self.channel.basic_publish(
                self.exchange,
                self.routing_key,
                message,
                pika.BasicProperties(
                    content_type='text/plain',
                    delivery_mode=pika.DeliveryMode.Persistent,
                    headers=headers
                ),
            )
        except AMQPError:
            self._channel()

    def stop(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close()


rmq: Optional[RabbitMQ] = None


def instance() -> RabbitMQ:
    return rmq
