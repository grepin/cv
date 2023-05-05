from datetime import datetime

import requests
from core.config import settings
from providers import (CancelPaymentResponse, CheckPaymentResponse, RepayResponse,
                       PaymentProvider, PaymentStatus)
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException


class CloudPayments(PaymentProvider):

    def __init__(self, *args, **kwargs):
        self.public_id = settings.CLOUDPAYMENTS_PUBLIC_ID
        self.api_key = settings.CLOUDPAYMENTS_API_KEY
        self.base_url = 'https://api.cloudpayments.ru/'
        self.check_payment_url = self.base_url + 'v2/payments/find'
        self.refund_payment_url = self.base_url + 'payments/refund'
        self.repay_payment_url = self.base_url + 'payments/tokens/charge'
        self.basic = HTTPBasicAuth(self.public_id.strip(), self.api_key.strip())
        self.headers = {'Content-Type': 'application/json'}

    def check_payment(self, sid: str) -> CheckPaymentResponse:
        try:
            r = requests.post(
                self.check_payment_url,
                headers=self.headers,
                json={"InvoiceId": sid},
                timeout=5,
                auth=self.basic,
            )
            data = r.json()
            if data['Success'] is False:
                if data['Message'] is not None:
                    return CheckPaymentResponse(
                        id=sid,
                        message='Not found',
                        datetime=datetime.utcnow(),
                        status=PaymentStatus.NOT_FOUND,
                        tid="",
                        token="",
                        raw=data)
                else:
                    s = PaymentStatus.DECLINED if data['Model']['Status'] == 'Declined' else PaymentStatus.PROCESSING
                    return CheckPaymentResponse(
                        id=sid,
                        message=data['Model']['Status'],
                        datetime=data['Model']['CreatedDateIso'],
                        status=s,
                        tid=data['Model']['TransactionId'],
                        token="",
                        raw=data)
            else:
                return CheckPaymentResponse(
                    id=sid,
                    message=data['Model']['Status'],
                    datetime=data['Model']['CreatedDateIso'],
                    status=PaymentStatus.COMPLETED,
                    tid=data['Model']['TransactionId'],
                    token=data['Model']['Token'],
                    raw=data)
        except RequestException as e:
            raise AssertionError("cloudpayments service problem: {}".format(e))

    def cancel_payment(self, tid: str, *args, **kwargs) -> CancelPaymentResponse:
        try:
            sid = kwargs["sid"]
            r = requests.post(
                self.refund_payment_url,
                headers=self.headers,
                json={"TransactionId": tid, "Amount": kwargs["price"]},
                timeout=5,
                auth=self.basic,
            )
            data = r.json()
            if data['Success'] is False:
                return CancelPaymentResponse(
                    id=sid,
                    message=data['Message'],
                    datetime=datetime.utcnow(),
                    status=PaymentStatus.DECLINED,
                    tid=tid,
                    raw=data)
            else:
                return CancelPaymentResponse(
                    id=sid,
                    message='refunded',
                    datetime=datetime.utcnow(),
                    status=PaymentStatus.REFUNDED,
                    tid=data['Model']['TransactionId'],
                    raw=data)
        except RequestException as e:
            raise AssertionError("cloudpayments service problem: {}".format(e))

    def repay(self, token: str, sid: str, uid: str, amount: str, currency: str) ->RepayResponse:
        try:
            r = requests.post(
                self.repay_payment_url,
                headers=self.headers,
                json={
                    "Currency": currency,
                    "Amount": amount,
                    "AccountId": uid,
                    "Token": token,
                    "InvoiceId": sid
                },
                timeout=5,
                auth=self.basic,
            )
            data = r.json()
            if data['Success'] is False:
                return RepayResponse(
                    id=sid,
                    message=data['Message'],
                    datetime=datetime.utcnow(),
                    status=PaymentStatus.DECLINED,
                    tid=data['Model']['TransactionId'],
                    raw=data)
            else:
                return RepayResponse(
                    id=sid,
                    message='repayed',
                    datetime=datetime.utcnow(),
                    status=PaymentStatus.REPAID,
                    tid=data['Model']['TransactionId'],
                    raw=data)
        except RequestException as e:
            raise AssertionError("cloudpayments service problem: {}".format(e))
