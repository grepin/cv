from uuid import UUID

from pydantic import BaseModel


class PaidNotification(BaseModel):
    user_id: UUID
    subscription_id: UUID
    provider: str = "providers.cloudpayments.CloudPayments"
    success: bool
    message: str
    code: int

    class Config:
        json_encoders = {
            UUID: lambda v: str(v),
        }


class CancelNotification(BaseModel):
    user_id: UUID
    subscription_id: UUID
    provider: str = "providers.cloudpayments.CloudPayments"

    class Config:
        json_encoders = {
            UUID: lambda v: str(v),
        }


class RepaymentNotification(BaseModel):
    user_id: UUID
    subscription_id: UUID
    provider: str = "providers.cloudpayments.CloudPayments"

    class Config:
        json_encoders = {
            UUID: lambda v: str(v),
        }
