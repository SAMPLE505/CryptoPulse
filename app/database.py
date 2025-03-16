from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv


# Подключение к БД
#getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/crypto_db")
DATABASE_URL = "postgresql://postgres:password@localhost:5432/crypto_db"


# Настройка SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Инициализация БД
def init_db():
    from app.models.user import User
    #from models.subscription import Subscription
    #from models.cryptocurrency import Cryptocurrency
    #from models.alert import Alert
    Base.metadata.create_all(bind=engine)


# Функция подмены БД в случае тестов
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()