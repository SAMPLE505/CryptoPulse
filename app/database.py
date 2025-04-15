from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings


# Получение адреса БД
DATABASE_URL = settings.DATABASE_URL


# Настройка SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Инициализация БД
def init_db():
    from app.models.user import User
    from app.models.subscription import Subscription
    #from models.alert import Alert
    Base.metadata.create_all(bind=engine)


# Функция подмены БД в случае тестов
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()