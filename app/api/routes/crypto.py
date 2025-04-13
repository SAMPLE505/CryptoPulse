from fastapi import APIRouter, HTTPException
from app.schemas.crypto import CryptoPriceResponseSchema, CryptoListResponseSchema
from app.services.crypto_service import get_cryptocurrency_price, get_cryptocurrency_list
from app.exceptions import CoinSymbolNotFound
from httpx import TimeoutException, HTTPError


crypto_router = APIRouter(prefix='/crypto')


# Эндпоинт получение курса выбранной монеты
@crypto_router.get("/price", tags=["Криптовалюта"])
async def get_coin_price(symbol: str) -> CryptoPriceResponseSchema:
    try:
        price = await get_cryptocurrency_price(symbol=symbol)
        return CryptoPriceResponseSchema(
            symbol=symbol,
            price=price
        )
    except CoinSymbolNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except TimeoutException:
        raise HTTPException(status_code=504, detail="CoinMarketCap API request timed out")
    
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=f"API request error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# Эндпоинт получение списка монет
@crypto_router.get("/list", tags=["Криптовалюта"])
async def get_coins_list() -> CryptoListResponseSchema:
    try:
        crypto_list = await get_cryptocurrency_list()
        return CryptoListResponseSchema(data=crypto_list)
    
    except TimeoutException:
        raise HTTPException(status_code=504, detail="CoinMarketCap API request timed out")
    
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=f"API request error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")