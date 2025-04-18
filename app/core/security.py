from uuid import UUID, uuid4
from jwt import decode, encode, ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.settings import settings
from app.models.user import User
from app.database import get_db


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_TTL_MINUTES = settings.ACCESS_TOKEN_TTL_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Токен будет ожидаться в Authorization: Bearer <token>


# Исключение на случай неудачной проверки токена
CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Функция хэширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Функция проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция аутентификации пользователя
def authenticate_user(username: str, password: str, db: Session) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Создание Access-токена
def create_access_token(data: dict, expire_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expire_delta or timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES))
    to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Создание Refresh-токена
def create_refresh_token(user_id: str) -> str:
    refresh_token = str(uuid4())
    return refresh_token


# Проверка Access-токена
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
