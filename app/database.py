from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv
from dotenv import load_dotenv


load_dotenv()


# Получение адреса БД
DATABASE_URL = getenv("DATABASE_URL")


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