from fastapi import FastAPI
from uvicorn import run
from contextlib import asynccontextmanager
from app.database import init_db
from app.api.routes.auth import auth_router
from app.api.routes.crypto import crypto_router
from app.services.background_tasks import update_crypto_list
from asyncio import create_task


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup: инициализируем базу данных, подключаем фоновые задачи
    init_db()
    create_task(update_crypto_list())
    yield
    # Shutdown: можно добавить логику завершения работы, если нужно


app = FastAPI(lifespan=lifespan)


# Подключение роутеров с эндпоинтами
app.include_router(auth_router)
app.include_router(crypto_router)


# uvicorn app.main:app --reload
if __name__ == "__main__":
    run("app.main:app", host="127.0.0.1", port=8000, reload=True)