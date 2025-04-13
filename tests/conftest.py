import pytest
from os import environ
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings


environ["ENV"] = 'test'
from app.main import app
from app.database import Base, get_db


# Используется тестовая БД PostgreSQL
TEST_DATABASE_URL = settings.DATABASE_URL


# Создание движка БД
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для настройки тестовой БД
@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


# Фикстура для замены БД на тестовую и создания тестового клиента
@pytest.fixture()
def test_client(test_db):
    def _get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = _get_test_db
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()