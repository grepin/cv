import uuid
from datetime import datetime

from db.postgres import Base
from sqlalchemy import FLOAT, Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSON


class Price(Base):
    __tablename__ = "price"
    __table_args__ = {"schema": "customers"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    duration = Column(FLOAT, nullable=False)
    price = Column(FLOAT, nullable=False)
    currency = Column(Enum("$", "rub"), default="rub", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    admin_id = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Price {self.duration} day {self.price} {self.currency}>"


class Subscription(Base):
    __tablename__ = "subscribtion"
    __table_args__ = {"schema": "customers"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    invoce_created = Column(DateTime, onupdate=datetime.utcnow)
    payment_datetime = Column(DateTime, nullable=False)
    start_subscribtion = Column(DateTime, nullable=False)
    subscribtion_expiration_datetime = Column(DateTime, nullable=False)
    payment_status = Column(Enum("invoce_created", "payment_completed", "payment_canceled"),
                            default="invoce_created", nullable=False)
    price_id = Column(UUID(as_uuid=True), ForeignKey("customers.price.id"), nullable=False)
    auto_renewal = Column(Boolean, default=False)
    transaction_id = Column(String(512))
    payment_token = Column(String(512))

    def __repr__(self):
        return f"<Subscription {self.id}>"


class PaymentsLog(Base):
    __tablename__ = "payments_log"
    __table_args__ = {"schema": "customers"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("customers.subscribtion.id"), nullable=False)
    event_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    provider = Column(String, nullable=False)
    status = Column(String, nullable=False)
    raw = Column(JSON)

    def __repr__(self):
        return f"<PaymentsLog {self.id}>"
