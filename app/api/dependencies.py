from jwt import decode, ExpiredSignatureError, InvalidTokenError
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Токен будет ожидаться в Authorization: Bearer <token>


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


# Исключение на случай неудачной проверки токена
CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Функция проверки JWT-токена пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise CredentialsException
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise CredentialsException

    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if user is None:
        raise CredentialsException
    return user