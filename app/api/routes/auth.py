from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token, create_refresh_token, authenticate_user
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
def login_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> LoginResponseSchema:
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
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
        secure=False, # Потом поменять на True с переходом на HTTPS
        samesite="strict",
        max_age=30 * 24 * 60 * 60 # 30 дней
    )

    return LoginResponseSchema(
        access_token=access_token,
        token_type='bearer',
        expires_in=900
        ).model_dump()