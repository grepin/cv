import base64
import json
from uuid import UUID

import sjwt
from core.config import settings
from db.postgres import get_db
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.errors_responses import (CONFLICT_409, NOT_FOUND_404,
                                      UNAUTHORIZED_401)
from schemas.schemas_postgres import FullSubscription, Price, Subscription, PaymentsLog
from schemas.schemas_requests import (ChangeMySubscription,
                                      StatusPaymentToPaid, SubsribeMe)
from schemas.schemas_response import PayRedirect, StatusResponseFromPaidEnum
from services.prices import get_price, get_prices
from services.pay_logs import get_my_pay_logs
from services.subscriptions import (get_my_subscription,
                                    path_to_change_subscription_payment_status,
                                    post_subscription_to_db, req_payservice,
                                    req_payservice_path_status)
from sqlalchemy.orm import Session

router = APIRouter()
security = HTTPBearer(auto_error=False)


def get_payload_from_jwt(bearer: HTTPAuthorizationCredentials = Security(security)):
    if not bearer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZED_401)
    payload = sjwt.checktoken.get_payload(key=settings.JWT_KEY, token=bearer.credentials)
    if not payload or (payload["Check_token"] is not True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZED_401)
    return payload


@router.get(
    "/",
    response_class=ORJSONResponse,
    summary="Посмотреть доступные подписки",
    description="Возвращает список активных подписок",
    response_model=list[Price],
    response_description="",
    tags=["subscription"]
)
def get_all_subscriptions(
        payload=Depends(get_payload_from_jwt),
        db: Session = Depends(get_db)
):
    if payload and payload["user_id"]:
        subscriptions = get_prices(db)
        if subscriptions is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_404)
        return subscriptions


@router.get(
    "/{sub_id}/",
    response_class=ORJSONResponse,
    summary="Посмотреть конкретную подписку",
    description="Возвращает подписоку по ее ID",
    response_model=Price,
    response_description="",
    tags=["subscription"]
)
def get_subscription(
        sub_id: UUID,
        payload=Depends(get_payload_from_jwt),
        db: Session = Depends(get_db)
):
    if payload and payload["user_id"]:
        subscription = get_price(db, sub_id)
        if subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_404)
        return subscription


@router.get(
    "/my/subscription/",
    response_class=ORJSONResponse,
    summary="Посмотреть подписку пользователя",
    description="Возвращает подписку по ID пользователя",
    response_model=FullSubscription,
    response_description="",
    tags=["subscription"]
)
def get_user_subscription(
        payload=Depends(get_payload_from_jwt),
        db: Session = Depends(get_db)
):
    if payload and payload["user_id"]:
        subscription = get_my_subscription(db, payload["user_id"])
        if subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_404)
        return subscription


@router.post(
    "/my/subscription/",
    response_class=ORJSONResponse,
    summary="Оформить подписку пользователя",
    description="Оформляет подписку по ID пользователя и ID выбранной подписки",
    response_model=PayRedirect,
    response_description="",
    tags=["subscription"]
)
def subscribe(
        boby: SubsribeMe,
        payload=Depends(get_payload_from_jwt),
        db: Session = Depends(get_db)
):
    if payload and payload["user_id"]:
        subscription = get_price(db, boby.subscription_id)
        subscription_id = post_subscription_to_db(
            db,
            payload["user_id"],
            boby.subscription_id,
            boby.start_date,
            subscription.duration,
            boby.auto_renewal
        ).id
        body_to_paid = {
            "user_id": payload["user_id"],
            "subscription_id": str(subscription_id),
            "provider": "providers.cloudpayments.CloudPayments",
            "success": True,
            "message": f"start date:{boby.start_date}",
            "code": StatusPaymentToPaid.message_code,
        }
        response_from_pay = req_payservice(body_to_paid)
        body_to_hash = {
            "template": "cloudpayments.html",
            "on_completed_callback": f"{settings.EXTERNAL_PAY_API_URL}/api/v1/paid/",
            "description": "Оплата подписки в pycinema.ru",
            "price": subscription.price,
            "currency": subscription.currency,
            "user_id": str(payload["user_id"]),
            "subscription_id": str(subscription_id),
            "email": payload["user_email"],
            "language": "ru-RU",
            "data": {"referer": boby.referer}
        }
        dict_to_bytes = json.dumps(body_to_hash).encode("utf-8")
        get_hash = base64.urlsafe_b64encode(dict_to_bytes)
        if response_from_pay and response_from_pay["status"] == StatusResponseFromPaidEnum.status_success:
            response_to_user_redirect = {
                "type": "redirect",
                "message": f"{settings.EXTERNAL_PAY_API_URL}/api/v1/pay/{str(get_hash)[2:-1]}",
                "response_from_pay": response_from_pay["status"]
            }
            return response_to_user_redirect
        else:
            response_to_user_redirect_unsuccess_payservice = {
                "type": "redirect",
                "message": f"{settings.EXTERNAL_PAY_API_URL}/api/v1/pay/{str(get_hash)[2:-1]}",
                "response_from_pay": "unsuccess from payservice"
            }
            return response_to_user_redirect_unsuccess_payservice


@router.patch(
    "/my/subscription/",
    response_class=ORJSONResponse,
    summary="Сменить статус подписки пользователя",
    description="",
    response_model=Subscription,
    response_description="",
    tags=["subscription"]
)
def change_my_subscription(
        boby: ChangeMySubscription,
        payload=Depends(get_payload_from_jwt),
        db: Session = Depends(get_db)
):
    if payload and payload["user_id"]:
        body_to_change_payment_status = {
            "user_id": payload["user_id"],
            "subscription_id": str(boby.subscription_id),
            "provider": "providers.cloudpayments.CloudPayments"
        }
        response_from_change_payment_status = req_payservice_path_status(body_to_change_payment_status)
        if response_from_change_payment_status and response_from_change_payment_status["status"] == StatusResponseFromPaidEnum.status_success:
            updated_user_subscription = path_to_change_subscription_payment_status(
                db,
                payload["user_id"],
                boby.subscription_id,
                boby.payment_status
            )
            return updated_user_subscription
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=CONFLICT_409)


@router.get(
    "/my/payment-logs/",
    response_class=ORJSONResponse,
    summary="Посмотреть оплата пользователя",
    description="Возврадащает логи оплат по ID пользователя",
    response_model=list[PaymentsLog],
    response_description="",
    tags=["subscription"]
)
def get_user_payment_logs(
        payload=Depends(get_payload_from_jwt),
        db: Session = Depends(get_db)
):
    if payload and payload["user_id"]:
        pay_logs = get_my_pay_logs(db, payload["user_id"])
        if pay_logs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_404)
        return pay_logs
