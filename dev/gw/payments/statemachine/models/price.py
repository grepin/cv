import uuid
from enum import Enum

from models import Base
from sqlalchemy import FLOAT, Boolean, Column, DateTime
from sqlalchemy import Enum as EnumColtype
from sqlalchemy import Integer, String, func
from sqlalchemy.dialects.postgresql import UUID


class Currency(Enum):
    dollar = "$"
    rub = "rub"


class Price(Base):
    __tablename__ = 'price'
    __table_args__ = {"schema": "customers"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(FLOAT, nullable=False)
    currency = Column(EnumColtype(Currency), default=Currency.rub, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    admin_id = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    updated_at = Column(DateTime, onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<Price {self.duration} day {self.price} {self.currency}>'
