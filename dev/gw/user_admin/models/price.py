import uuid
from datetime import datetime
from enum import Enum

from db.postgres import db
from sqlalchemy import UniqueConstraint  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


class Currency(Enum):
    dollar = "$"
    rub = "RUB"


class Price(db.Model):
    __tablename__ = 'price'
    __table_args__ = {"schema": "customers"}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    duration = db.Column(db.FLOAT, nullable=False)
    price = db.Column(db.FLOAT, nullable=False)
    currency = db.Column(db.Enum(Currency), default=Currency.rub, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    admin_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Price {self.duration} day {self.price} {self.currency}>'
