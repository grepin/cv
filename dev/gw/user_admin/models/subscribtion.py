import uuid
from datetime import datetime
from enum import Enum

from db.postgres import db
from sqlalchemy import UniqueConstraint  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


class StatusSubsribtion(Enum):
    invoce_created = "invoce_created"
    payment_completed = "payment_completed"
    payment_canceled = "payment_canceled"


class Subscribtion(db.Model):
    __tablename__ = 'subscribtion'
    __table_args__ = {"schema": "customers"}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.user.id'), nullable=False)
    invoce_created = db.Column(db.DateTime, onupdate=datetime.utcnow)
    payment_datetime = db.Column(db.DateTime, nullable=False)
    start_subscribtion = db.Column(db.DateTime, nullable=False)
    subscribtion_expiration_datetime = db.Column(db.DateTime, nullable=False)
    # subscription_duration = db.Column(db.Integer, nullable=False)
    # price = db.Column(db.FLOAT, nullable=False)
    # currency = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.Enum(StatusSubsribtion), default=StatusSubsribtion.invoce_created, nullable=False)
    price_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.price.id'), nullable=False)


    def __repr__(self):
        return f'<Subscribtion {self.id}>'