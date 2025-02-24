from fastapi import Depends, APIRouter, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from schemas.user import UserRegistrationSchema


router = APIRouter()


# Эндпоинт получения текущей погоды по координатам
@router.post("/auth/register", tags=["Аутентификация"])
async def register_user(user: UserRegistrationSchema, db: Session = Depends(get_db)):
    # Логика регистрации пользователя
    # Если пользователь уже существует, можно вернуть ошибку:
    # raise HTTPException(status_code=400, detail="Пользователь уже существует")
    return {"message": "Пользователь успешно зарегистрирован", "user": user.model_dump()}