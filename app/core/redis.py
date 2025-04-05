import redis
from dotenv import load_dotenv
from os import getenv
from datetime import timedelta
from typing import List
import json


load_dotenv()

REFRESH_TOKEN_TTL_DAYS = int(getenv("REFRESH_TOKEN_TTL_DAYS"))
CRYPTO_PRICE_TTL_SECONDS = int(getenv("CRYPTO_PRICE_TTL_SECONDS"))
CRYPTO_LIST_TTL_MINUTES = int(getenv("CRYPTO_LIST_TTL_MINUTES"))

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


# Сохранение refresh-токена JWT
def store_token(user_id: str, token: str, ttl: int = REFRESH_TOKEN_TTL_DAYS):
    redis_client.setex(f"token:{user_id}", timedelta(days=ttl), token)


# Получение refresh-токена JWT
def get_token(user_id: str):
    return redis_client.get(f"token:{user_id}")


# Удаление refresh-токена JWT
def delete_token(user_id: str):
    redis_client.delete(f"token:{user_id}")


# Сохранение цены валюты
def store_crypto_price(symbol: str, price: float, ttl: int = CRYPTO_PRICE_TTL_SECONDS):
    redis_key = f"price:{symbol.upper()}"
    redis_client.setex(redis_key, ttl, str(price))


# Получение цены валюты
def get_crypto_price(symbol: str) -> float | None:
    redis_key = f"price:{symbol.upper()}"
    value = redis_client.get(redis_key)
    return float(value) if value is not None else None


# Сохранение списка валют
def store_crypto_list(crypto_list: list, ttl: int = CRYPTO_LIST_TTL_MINUTES):
    redis_client.setex("crypto:list", timedelta(minutes=ttl), json.dumps(crypto_list))


# Получение списка валют
def get_crypto_list():
    crypto_list = redis_client.get("crypto:list")
    if crypto_list:
        return json.loads(crypto_list)
    return None
