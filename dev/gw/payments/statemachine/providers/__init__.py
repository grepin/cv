from __future__ import annotations

from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from importlib import import_module

from pydantic import BaseModel


class PaymentStatus(Enum):
    NOT_FOUND = 'not found'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    DECLINED = 'declined'
    REFUNDED = 'refunded'
    REPAID = 'repaid'


class CheckPaymentResponse(BaseModel):
    id: str
    message: str
    datetime: datetime
    status: PaymentStatus
    tid: str
    token: str
    raw: dict

    class Config:
        use_enum_values = True


class CancelPaymentResponse(BaseModel):
    id: str
    message: str
    datetime: datetime
    status: PaymentStatus
    tid: str
    raw: dict

    class Config:
        use_enum_values = True


class RepayResponse(BaseModel):
    id: str
    message: str
    datetime: datetime
    status: PaymentStatus
    tid: str
    raw: dict

    class Config:
        use_enum_values = True


class PaymentProvider(metaclass=ABCMeta):
    @abstractmethod
    def check_payment(self, sid: str) -> CheckPaymentResponse:
        pass

    @abstractmethod
    def cancel_payment(self, tid: str, *args, **kwargs) -> CancelPaymentResponse:
        pass

    @abstractmethod
    def repay(self, token: str, sid: str, uid: str, amount: str, currency: str) -> RepayResponse:
        pass

    @staticmethod
    def instance(classname: str = None, *args, **kwargs) -> PaymentProvider:
        try:
            module_path, class_name = classname.rsplit('.', 1)
            assert module_path.startswith('providers')
            module = import_module(module_path)
            return getattr(module, class_name)(args, kwargs)
        except (ImportError, AttributeError, AssertionError) as e:
            raise Exception(e)
