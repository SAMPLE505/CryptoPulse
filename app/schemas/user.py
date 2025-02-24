from pydantic import BaseModel

# Пример Pydantic-схемы для регистрации
class UserRegistrationSchema(BaseModel):
    email: str
    password: str
    full_name: str = None