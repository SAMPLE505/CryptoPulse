import redis
from dotenv import load_dotenv
from os import getenv
from datetime import timedelta

load_dotenv()

REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def store_token(user_id: str, token: str, expire_delta: timedelta = None):
    expire = expire_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    redis_client.setex(f"token:{user_id}", expire, token)


def get_token(user_id: str):
    return redis_client.get(f"token:{user_id}")


def delete_token(user_id: str):
    redis_client.delete(f"token:{user_id}")