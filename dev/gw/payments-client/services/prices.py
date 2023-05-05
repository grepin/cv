from uuid import UUID

from models.models import Price as PriceModel
from sqlalchemy.orm import Session


def get_price(db: Session, price_id: UUID):
    return db.query(PriceModel).filter(PriceModel.id == price_id).first()


def get_prices(db: Session):
    return db.query(PriceModel).filter(PriceModel.is_active == True).all()
