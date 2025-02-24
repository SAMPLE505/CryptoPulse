from pydantic import BaseModel
from uuid import UUID


# Pydantic-схема запроса на регистрацию пользователя
class UserRegistrationSchema(BaseModel):
    email: str
    password: str
    full_name: str = None


# Pydantic-схема ответа об успешной регистрации пользователя
class UserResponseSchema(BaseModel):
    id: UUID
    email: str
    full_name: str = None