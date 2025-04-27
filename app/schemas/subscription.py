from pydantic import BaseModel
from uuid import UUID


# Схема запроса с информацией о подписке
class SubscriptionCreateSchema(BaseModel):
    symbol: str
    threshold: float
    above: bool


# Схема запроса с информацией об обновлении подписки
class SubscriptionUpdateSchema(BaseModel):
    threshold: float
    above: bool


class SubscriptionResponseSchema(BaseModel):
    id: UUID
    symbol: str
    threshold: float
    above: bool

    model_config = {
        "from_attributes": True
    }