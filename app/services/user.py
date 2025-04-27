from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserRegistrationSchema, RegistrationResponseSchema
from app.core.security import get_password_hash


# Функция добавления пользователя в БД
def add_user(user_data: UserRegistrationSchema, db: Session) -> RegistrationResponseSchema:
    
    # Проверка существования пользователя с таким email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Создание объекта пользователя
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        username=user_data.username
    )

    # Добавляем в БД
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Возвращаем данные без пароля
    return RegistrationResponseSchema(id=new_user.id, email=new_user.email, username=new_user.username)
