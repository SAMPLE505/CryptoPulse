from fastapi import APIRouter, HTTPException
from app.schemas.crypto import CryptoRateResponseSchema
from app.services.crypto_service import get_cryptocurrency_price
from app.exceptions import CoinSymbolNotFound
from httpx import TimeoutException, HTTPError

crypto_router = APIRouter(prefix='/crypto')

# Эндпоинт регистрации пользователя
@crypto_router.get("/getcoinprice", tags=["Криптовалюта"])
async def get_coin_price(coin_symbol: str) -> CryptoRateResponseSchema:
    try:
        price = await get_cryptocurrency_price(coin_symbol=coin_symbol)
        return CryptoRateResponseSchema(
            coin_symbol=coin_symbol,
            price=price
        )
    except CoinSymbolNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except TimeoutException:
        raise HTTPException(status_code=503, detail="CoinMarketCap API request timed out")
    
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=f"API request error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")