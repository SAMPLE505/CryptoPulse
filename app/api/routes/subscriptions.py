from fastapi import Depends, APIRouter, HTTPException, Response
from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from sqlalchemy.orm import Session


subscriptions_router = APIRouter(prefix='/subscriptions')


# Эндпоинт создания новой подписки
@subscriptions_router.post("/", tags=["Подписки"])
async def create_subscription(user_data: dict, db: Session = Depends(get_db)):
    return None


# Эндпоинт получения всех подписок пользователя
@subscriptions_router.get("/", tags=["Подписки"])
async def get_subscriptions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"user_id": user.id, "message": "Your subscriptions here"}


# Эндпоинт получения выбранной подписки
@subscriptions_router.get("/{subscription_id}", tags=["Подписки"])
async def get_subscription(user_data: dict, db: Session = Depends(get_db)):
    return None


# Эндпоинт обновления подписки
@subscriptions_router.put("/{subscription_id}", tags=["Подписки"])
async def update_subscription(user_data: dict, db: Session = Depends(get_db)):
    return None


# Эндпоинт удаления подписки
@subscriptions_router.get("/{subscription_id}", tags=["Подписки"])
async def delete_subscription(user_data: dict, db: Session = Depends(get_db)):
    return None


# Эндпоинт активации/деактивации подписки
@subscriptions_router.post("/{subscription_id}/toggle", tags=["Подписки"])
async def toggle_subscription(user_data: dict, db: Session = Depends(get_db)):
    return None