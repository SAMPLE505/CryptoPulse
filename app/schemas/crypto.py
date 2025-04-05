from pydantic import BaseModel
from typing import List


# Pydantic-схема ответа с курсом валюты в USDT
class CryptoPriceResponseSchema(BaseModel):
    symbol: str
    price: float


# Pydantic-схема ответа с курсом валюты в USDT
class CryptoListResponseSchema(BaseModel):
    data: List