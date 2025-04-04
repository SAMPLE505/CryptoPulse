from pydantic import BaseModel, EmailStr
from uuid import UUID


# Pydantic-схема запроса для регистрацию пользователя
class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    username: str = None


# Pydantic-схема запроса для авторизации пользователя
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


# Pydantic-схема ответа об успешной регистрации пользователя
class RegistrationResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    username: str = None

# Pydantic-схема ответа об успешной авторизации пользователя
class LoginResponseSchema(BaseModel):
    access: str
    token_type: str
    expires_in: int