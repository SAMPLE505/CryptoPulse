import uuid
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.settings import settings
from app.models.user import User


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_TTL_MINUTES = settings.ACCESS_TOKEN_TTL_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция хэширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Функция проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция аутентификации пользователя
def authenticate_user(username: str, password: str, db: Session):
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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Создание Refresh-токена
def create_refresh_token(user_id: str) -> str:
    refresh_token = str(uuid.uuid4())
    return refresh_token


# Расшифровка Access-токена
def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
