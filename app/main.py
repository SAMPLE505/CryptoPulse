from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager
from app.database import init_db
from app.api.routes.auth import router as auth_router



@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup: инициализируем базу данных
    init_db()
    yield
    # Shutdown: можно добавить логику завершения работы, если нужно


app = FastAPI(lifespan=lifespan)


# Подключаем роутер с эндпоинтами для аутентификации
app.include_router(auth_router)


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)