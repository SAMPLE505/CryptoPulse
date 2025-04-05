from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLoginSchema, UserRegistrationSchema, LoginResponseSchema
from app.services.user import add_user
from app.core.redis import store_token


auth_router = APIRouter(prefix='/auth')


# Эндпоинт регистрации пользователя
@auth_router.post("/register", tags=["Аутентификация"])
async def register_user(user_data: UserRegistrationSchema, db: Session = Depends(get_db)):
    response = add_user(user_data=user_data, db=db)
    return {"message": "User successfully registered", "user": response.model_dump()}


# Эндпоинт аутентификации и авторизации пользователя
@auth_router.post("/login", tags=["Аутентификация"])
def login_user(user_data: UserLoginSchema, response: Response, db: Session = Depends(get_db)) -> LoginResponseSchema:
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Создание JWT-токенов
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(user.id)

    # Сохранение Refresh-токена в Redis
    store_token(str(user.id), refresh_token)

    # Установка cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False, # Потом поменять на True с переходом на HTTP
        samesite="strict",
        max_age=30 * 24 * 60 * 60 # 30 дней
    )

    return LoginResponseSchema(
        access=access_token,
        token_type='bearer',
        expires_in=900
        ).model_dump()