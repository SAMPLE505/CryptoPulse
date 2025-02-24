from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegistrationSchema
from app.services.user import add_user


router = APIRouter()


# Эндпоинт регистрации пользователя
@router.post("/auth/register", tags=["Аутентификация"])
async def register_user(user: UserRegistrationSchema, db: Session = Depends(get_db)):
    response = add_user(user_data=user, db=db)
    return {"message": "User successfully registered", "user": response.model_dump()}