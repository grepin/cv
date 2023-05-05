from uuid import UUID

from models.models import PaymentsLog
from models.models import Subscription as SubscriptionModel
from sqlalchemy.orm import Session
from sqlalchemy import desc


def get_my_pay_logs(
    db: Session,
    user_id: UUID
) -> list[PaymentsLog] | None:
    user_pay_logs = db.query(PaymentsLog).join(SubscriptionModel).filter(SubscriptionModel.user_id == user_id).order_by(desc(PaymentsLog.event_time)).all()
    if user_pay_logs is None:
        return None
    return user_pay_logs
