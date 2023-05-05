from enum import Enum

from pydantic import BaseModel


class PayRedirect(BaseModel):
    type: str
    message: str
    response_from_pay: str


class StatusResponseFromPaidEnum(str, Enum):
    status_success = "success"
