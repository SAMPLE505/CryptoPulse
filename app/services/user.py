from sqlalchemy.orm import Session
from fastapi import HTTPException
#from passlib.context import CryptContext
from uuid import uuid4
from app.models.user import User
from app.schemas.user import UserRegistrationSchema, UserResponseSchema
from app.core.security import get_password_hash


# Функция добавления пользователя в БД
def add_user(user_data: UserRegistrationSchema, db: Session) -> UserResponseSchema:
    
    # Проверка существования пользователя с таким email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Создание объекта пользователя
    new_user = User(
        id=uuid4(),
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name
    )

    # Добавляем в БД
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Возвращаем данные без пароля
    return UserResponseSchema(id=new_user.id, email=new_user.email, full_name=new_user.full_name)