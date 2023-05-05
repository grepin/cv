from datetime import datetime
from enum import Enum
from uuid import UUID

import orjson
from pydantic import BaseModel


class CurrencyEnum(str, Enum):
    dollar = "$"
    rub = "rub"


class StatusSubsriptionEnum(str, Enum):
    invoce_created = "invoce_created"
    payment_completed = "payment_completed"
    payment_canceled = "payment_canceled"


class StatusPaymentToPaid(int, Enum):
    message_code = 777


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class SubsribeMe(BaseOrjsonModel):
    subscription_id: UUID
    start_date: datetime
    referer: str
    auto_renewal: bool = False


class ChangeMySubscription(BaseOrjsonModel):
    subscription_id: UUID
    payment_status: StatusSubsriptionEnum
