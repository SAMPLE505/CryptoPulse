from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция хэширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)