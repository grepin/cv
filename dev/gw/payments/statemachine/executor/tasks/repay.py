from datetime import datetime, timedelta
import logging

import executor.app as container
from executor.tasks import init_db
from models.payments_log import PaymentsLog
from models.price import Price
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
def repay(self, json: dict) -> None:
    global engine, session_maker
    session = None
    try:
        sid = json['subscription_id']
        provider_name = json['provider']
        engine, session_maker = init_db(engine, session_maker)
        session = session_maker()
        session.begin()
        sp = session.query(Subscribtion, Price).filter_by(id=sid).join(Price).one_or_none()
        if sp is None:
            logging.info("[{0}] no pre-created subscription found for sid = {1}".format(
                self.request.id,
                sid)
            )
            session.rollback()
            return
        sub, price = sp
        if sub.payment_status != StatusSubsribtion.payment_completed:
            logging.info("[{0}] no need to repay subscription for sid = {1}, {2}".format(
                self.request.id,
                sid,
                sub.payment_status.value)
            )
            session.rollback()
            return
        if sub.auto_renewal is not True:
            logging.info("[{0}] autorenewal is not set for sid = {1}, {2}".format(
                self.request.id,
                sid,
                sub.payment_status.value)
            )
            session.rollback()
            return
        session.commit()
        provider = PaymentProvider.instance(classname=provider_name)
        repay_payment_response = provider.repay(sub.payment_token, sid, str(sub.user_id), price.price, price.currency.value)
        sub = session.query(Subscribtion).filter_by(id=sid).one_or_none()
        if repay_payment_response.status == PaymentStatus.DECLINED.value:
            logging.info("[{0}] repay failed for transaction with tid = {1}, {2}".format(
                self.request.id,
                sub.transaction_id,
                repay_payment_response.status)
            )
            session.rollback()
            raise AssertionError
        if repay_payment_response.status == PaymentStatus.REPAID.value:
            sub.subscribtion_expiration_datetime = datetime.utcnow() + timedelta(days=price.duration)
            sub.transaction_id = repay_payment_response.tid
            logging.info("[{0}] repayment confirmed for transaction with tid = {1}, {2}".format(
                self.request.id,
                sub.transaction_id,
                repay_payment_response.status)
            )
        log = PaymentsLog(
            subscription_id=sid,
            provider=provider_name,
            status=repay_payment_response.status,
            raw=repay_payment_response.raw
        )
        session.add(log)
        session.commit()
        logging.info("[{0}] successfully repaid subscription for sid = {1}, {2}".format(
            self.request.id, sid, sub.payment_status.value)
        )
    finally:
        if session is not None:
            session.close()
        if self.request.retries == self.max_retries:
            logging.info("max retries reached, will stay with current state forever")
