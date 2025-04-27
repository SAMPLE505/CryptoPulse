from fastapi import Depends, APIRouter, HTTPException, Response
from uuid import UUID
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.subscription import SubscriptionCreateSchema, SubscriptionUpdateSchema, SubscriptionResponseSchema
from app.services.subscription import add_user_subscription, get_user_subscriptions, get_user_subscription, update_user_subscription, delete_user_subscription, toggle_user_subscription


subscriptions_router = APIRouter(prefix='/subscriptions')


# Эндпоинт создания новой подписки
@subscriptions_router.post("/", tags=["Подписки"], response_model = SubscriptionResponseSchema)
async def create_subscription(subscription_data: SubscriptionCreateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = add_user_subscription(
        user_id=user.id,
        symbol=subscription_data.symbol,
        threshold=subscription_data.threshold,
        above=subscription_data.above,
        db=db
    )
    return subscription


# Эндпоинт получения всех подписок пользователя
@subscriptions_router.get("/", tags=["Подписки"])
async def get_subscriptions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sub_list = get_user_subscriptions(user_id=user.id, db=db)
    return {"data": sub_list}


# Эндпоинт получения выбранной подписки
@subscriptions_router.get("/{subscription_id}", tags=["Подписки"], response_model = SubscriptionResponseSchema)
async def get_subscription(subscription_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = get_user_subscription(subscription_id=subscription_id, user_id=user.id, db=db)
    return subscription


# Эндпоинт обновления подписки
@subscriptions_router.put("/{subscription_id}", tags=["Подписки"])
async def update_subscription(subscription_id: UUID, updates: SubscriptionUpdateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = get_user_subscription(subscription_id=subscription_id, user_id=user.id, db=db)
    subscription = update_user_subscription(subscription=subscription, updates=updates, db=db)
    return subscription


# Эндпоинт удаления подписки
@subscriptions_router.delete("/{subscription_id}", tags=["Подписки"])
async def delete_subscription(subscription_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = get_user_subscription(subscription_id=subscription_id, user_id=user.id, db=db)
    delete_user_subscription(subscription=subscription, db=db)
    return {"message": "Subscription deleted successfully"}


# Эндпоинт активации/деактивации подписки
@subscriptions_router.post("/{subscription_id}/toggle", tags=["Подписки"])
async def toggle_subscription(subscription_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = get_user_subscription(subscription_id=subscription_id, user_id=user.id, db=db)
    subscription = toggle_user_subscription(subscription=subscription, db=db)
    return subscription