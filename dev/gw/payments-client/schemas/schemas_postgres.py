from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CurrencyEnum(str, Enum):
    dollar = "$"
    rub = "rub"


class StatusSubsriptionEnum(str, Enum):
    invoce_created = "invoce_created"
    payment_completed = "payment_completed"
    payment_canceled = "payment_canceled"


class Price(BaseModel):
    id: UUID
    duration: float
    price: float
    currency: CurrencyEnum
    created_at: datetime
    admin_id: str  # TODO: UUID
    is_active: bool
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class Subscription(BaseModel):
    id: UUID
    user_id: UUID
    invoce_created: Optional[datetime]
    payment_datetime: datetime
    start_subscribtion: datetime
    subscribtion_expiration_datetime: datetime
    payment_status: StatusSubsriptionEnum
    price_id: UUID
    auto_renewal: bool
    payment_token: str | None

    class Config:
        orm_mode = True


class FullSubscription(BaseModel):
    subscription: Subscription
    price: Price


class PaymentsLog(BaseModel):
    id: UUID
    subscription_id: UUID
    event_time: datetime
    provider: str
    status: str
    raw: dict | None

    class Config:
        orm_mode = True
