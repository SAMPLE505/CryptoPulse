from pydantic import BaseModel


# Pydantic-схема ответа с курсом валюты в USDT
class CryptoRateResponseSchema(BaseModel):
    coin_symbol: str
    price: float