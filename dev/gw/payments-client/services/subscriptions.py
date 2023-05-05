from datetime import datetime, timedelta
from uuid import UUID

import requests
from core.config import settings
from models.models import Price
from models.models import Subscription as SubscriptionModel
from sqlalchemy.orm import Session


def get_my_subscription(
    db: Session,
    user_id: UUID
) -> dict[str, SubscriptionModel | Price] | None:
    user_subscription = db.query(SubscriptionModel).filter(
        SubscriptionModel.user_id == user_id,
        SubscriptionModel.payment_status == "payment_completed",
        SubscriptionModel.start_subscribtion < datetime.now(),
        SubscriptionModel.subscribtion_expiration_datetime > datetime.now()).first()
    if user_subscription is None:
        return None
    user_price = db.query(Price).filter(
        Price.id == user_subscription.price_id).first()
    response = {"subscription": user_subscription, "price": user_price}
    return response


def post_subscription_to_db(
    db: Session,
    user_id: UUID,
    price_id: UUID,
    start_date: datetime,
    duration: float,
    auto_renewal: bool
) -> SubscriptionModel:
    db_sudcription = SubscriptionModel(
        user_id=user_id,
        invoce_created=datetime.now(),
        payment_datetime=datetime.now(),
        start_subscribtion=start_date,
        subscribtion_expiration_datetime=start_date + timedelta(days=duration),
        payment_status="invoce_created",
        auto_renewal=auto_renewal,
        price_id=price_id
    )
    db.add(db_sudcription)
    db.commit()
    db.refresh(db_sudcription)
    return db_sudcription


def path_to_change_subscription_payment_status(
    db: Session,
    user_id: UUID,
    subscription_id: UUID,
    payment_status: str
) -> SubscriptionModel:
    user_subscription = db.query(SubscriptionModel).filter(
        SubscriptionModel.user_id == user_id,
        SubscriptionModel.id == subscription_id).first()
    return user_subscription


def req_payservice(body: dict) -> dict | None:
    pay_service_path = f"{settings.INTERNAL_PAY_API_URL}/api/v1/paid/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response_from_pay = requests.post(pay_service_path, headers=headers, json=body, verify=False)
        return response_from_pay.json()
    except requests.exceptions.ConnectionError:
        return None


def req_payservice_path_status(body: dict) -> dict | None:
    cancel_service_path = f"{settings.INTERNAL_PAY_API_URL}/api/v1/cancel/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response_from_pay = requests.post(cancel_service_path, headers=headers, json=body, verify=False)
        return response_from_pay.json()
    except requests.exceptions.ConnectionError:
        return None
