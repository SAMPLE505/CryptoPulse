from os import getenv
from sqlalchemy import create_engine, Column, String, Float, Integer, JSON, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
from fastapi import FastAPI, Depends
from uvicorn import run

# Настройка базы данных SQLite
DATABASE_URL = "sqlite:///:memory:" if getenv("TEST") else "sqlite:///./crypto.db"

# Настройка SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()

Base.metadata.create_all(bind=engine)

# Функция получения 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)