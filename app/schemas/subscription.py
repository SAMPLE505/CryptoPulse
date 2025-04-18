from pydantic import BaseModel
from uuid import UUID

class SubscriptionCreateSchema(BaseModel):
    symbol: str
    threshold: float
    above: bool

class SubscriptionUpdateSchema(BaseModel):
    threshold: float
    above: bool

class SubscriptionResponseSchema(BaseModel):
    id: UUID
    symbol: str
    threshold: float
    above: bool

    class Config:
        orm_mode = True