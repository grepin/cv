import uuid

from models import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSON, UUID


class PaymentsLog(Base):
    __tablename__ = 'payments_log'
    __table_args__ = {"schema": "customers"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey('customers.subscribtion.id'), nullable=False)
    event_time = Column(DateTime, default=func.current_timestamp(), nullable=False)
    provider = Column(String, nullable=False)
    status = Column(String, nullable=False)
    raw = Column(JSON)

    def __repr__(self):
        return f'<PaymentsLog {self.id}>'
