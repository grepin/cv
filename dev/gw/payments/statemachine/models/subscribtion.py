import uuid
from datetime import datetime
from enum import Enum

from models import Base
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as EnumColtype
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID


class StatusSubsribtion(Enum):
    invoce_created = "invoce_created"
    payment_completed = "payment_completed"
    payment_canceled = "payment_canceled"


class Subscribtion(Base):
    __tablename__ = 'subscribtion'
    __table_args__ = {"schema": "customers"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    invoce_created = Column(DateTime, onupdate=datetime.utcnow)
    payment_datetime = Column(DateTime, nullable=False)
    start_subscribtion = Column(DateTime, nullable=False)
    subscribtion_expiration_datetime = Column(DateTime, nullable=False)
    payment_status = Column(EnumColtype(StatusSubsribtion), default=StatusSubsribtion.invoce_created, nullable=False)
    price_id = Column(UUID(as_uuid=True), ForeignKey('customers.price.id'), nullable=False)
    auto_renewal = Column(Boolean, default=False)
    transaction_id = Column(String(512))
    payment_token = Column(String(512))

    def __repr__(self):
        return f'<Subscribtion {self.id}>'
