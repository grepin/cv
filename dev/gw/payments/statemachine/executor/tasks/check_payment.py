import datetime
import logging

import executor.app as container
from executor.tasks import init_db
from models.payments_log import PaymentsLog
from models.subscribtion import StatusSubsribtion, Subscribtion
from providers import PaymentProvider, PaymentStatus
from sqlalchemy.exc import SQLAlchemyError

app = container.app
engine = None
session_maker = None


@app.task(
    bind=True,
    autoretry_for=(AssertionError, SQLAlchemyError),
    retry_backoff=15,
    max_retries=8,
    retry_jitter=False,
)
def check_payment(self, json: dict) -> None:
    global engine, session_maker
    session = None
    try:
        sid = json['subscription_id']
        provider_name = json['provider']
        provider = PaymentProvider.instance(classname=provider_name)
        check_payment_response = provider.check_payment(sid=sid)
        engine, session_maker = init_db(engine, session_maker)
        session = session_maker()
        session.begin()
        sub = session.query(Subscribtion).filter_by(id=sid).one_or_none()
        if sub is None:
            logging.info("no pre-created subscription found for sid = {0}".format(
                sid)
            )
            session.rollback()
            return
        if sub.payment_status != StatusSubsribtion.invoce_created:
            logging.info("no need to change subscription for sid = {0}, {1}".format(
                sid,
                sub.payment_status.value)
            )
            session.rollback()
            return
        if check_payment_response.status == PaymentStatus.NOT_FOUND.value:
            logging.info("no known by provider subscription for sid = {0}, {1}".format(
                sid,
                check_payment_response.status)
            )
            session.rollback()
            raise AssertionError
        if check_payment_response.status == PaymentStatus.PROCESSING.value:
            logging.info("subscription payment expected for sid = {0}, {1}".format(
                sid,
                check_payment_response.status)
            )
            log = PaymentsLog(
                subscription_id=sid,
                provider=provider_name,
                status=check_payment_response.status,
                raw=check_payment_response.raw
            )
            session.add(log)
            session.commit()
            raise AssertionError
        if check_payment_response.status == PaymentStatus.COMPLETED.value:
            sub.payment_status = StatusSubsribtion.payment_completed
            sub.payment_datetime = datetime.datetime.utcnow()
            sub.transaction_id = check_payment_response.tid
            sub.payment_token = check_payment_response.token
        if check_payment_response.status == PaymentStatus.DECLINED.value:
            sub.payment_status = StatusSubsribtion.payment_canceled
        log = PaymentsLog(
            subscription_id=sid,
            provider=provider_name,
            status=check_payment_response.status,
            raw=check_payment_response.raw
        )
        session.add(log)
        session.commit()
        logging.info("updated subscription for sid = {0}, {1}".format(sid, sub.payment_status.value))
    finally:
        if session is not None:
            session.close()
        if self.request.retries == self.max_retries:
            logging.info("max retries reached, will stay forever with this state")
