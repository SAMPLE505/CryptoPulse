from httpx import AsyncClient, TimeoutException, HTTPError
from dotenv import load_dotenv
from os import getenv
from app.core.redis import get_crypto_price, store_crypto_price
from app.exceptions import CoinSymbolNotFound


# Загрузка .env файла
load_dotenv()


# Загрузка ключа API CoinMarketCap
API_KEY = getenv("API_KEY")


# Функция получения цены криптовалюты в USD с API
async def get_cryptocurrency_price(coin_symbol: str):

    # Получение цены валюты из Redis
    cached = get_crypto_price(coin_symbol)
    if cached is not None:
        return cached
    
    try:
        # Запрос к API
        async with AsyncClient(timeout=10) as client:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
            params = {
                "start":"1",
                "limit":"5000",
                "sort":"id",
            }
            headers = {
                "Accepts": "application/json",
                "X-CMC_PRO_API_KEY": f"{API_KEY}",
            }
            response = await client.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()["data"]

            for entry in data:
                if entry["symbol"].upper() == coin_symbol.upper():
                    price = entry["quote"]["USD"]["price"]
                    store_crypto_price(coin_symbol, price) # Сохранение цены валюты в Redis
                    return price
            
            raise CoinSymbolNotFound(f"Coin symbol '{coin_symbol}' not found")
    
    except TimeoutException:
        raise Exception("The request to CoinMarketCap exceeded the time limit")
    
    except HTTPError as e:
        raise Exception(f"Error during API request: {str(e)}")