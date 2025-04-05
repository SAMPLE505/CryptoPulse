import asyncio
from app.services.crypto_service import get_cryptocurrency_list


# Функция для обновления списка криптовалют в фоновом режиме
async def update_crypto_list():
    while True:
        try:
            print("[UPDATER] Refreshing crypto list from API...")
            await get_cryptocurrency_list()
        except Exception as e:
            print(f"[UPDATER ERROR] {e}")
        await asyncio.sleep(3600)  # Обновление списка каждый час
    
