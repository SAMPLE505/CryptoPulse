from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


# Модель подписки на валюту
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String, nullable=False)  # Например, BTC, ETH
    threshold = Column(Float, nullable=True)  # Пороговое значение
    above = Column(Boolean, default=True)  # True: алерт при превышении порога, False: при падении ниже
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="subscriptions")
