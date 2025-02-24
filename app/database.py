from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv


# Адрес БД
DATABASE_URL = "sqlite:///:memory:" if getenv("TEST") else "sqlite:///./crypto.db"


# Настройка SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Инициализация БД
def init_db():
    from models.user import User
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