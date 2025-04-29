import asyncio
from app.services.crypto_service import get_cryptocurrency_list, get_cryptocurrency_price
from app.database import get_db
from app.models.subscription import Subscription


# Функция для обновления списка криптовалют в фоновом режиме
async def update_crypto_list():
    while True:
        try:
            print("[UPDATER] Refreshing crypto list from API...")
            await get_cryptocurrency_list()
        except Exception as e:
            print(f"[UPDATER ERROR] {e}")
        await asyncio.sleep(3600)  # Обновление списка каждый час


# Функция для уведомления обновления цен отслеживаемых валют в кэше в фоновом режиме
async def monitor_subscritptions():
    while True:
        try:
            with get_db() as db:

                print("[UPDATER] Refreshing cached crypto prices...")

                subscriptions = db.query(Subscription).filter(Subscription.is_active == True).all()

                if not subscriptions:
                    await asyncio.sleep(60)
                    continue
                
                # Группировка подписок по символу монеты
                subscriptions_by_symbol = {}
                for sub in subscriptions:
                    subscriptions_by_symbol.setdefault(sub.symbol.upper(), []).append(sub)

                # Обработка каждой валюты
                for symbol, subs in subscriptions_by_symbol.items():
                    price = await get_cryptocurrency_price(symbol)

                    for sub in subs:
                        if (sub.above and price > sub.threshold) or (not sub.above and price < sub.threshold):
                            pass
                            # await notify_user(user_id=sub.user_id, symbol=symbol, price=price, threshold=sub.threshold)

        except Exception as e:
            print(f"[UPDATER ERROR] {e}")

        await asyncio.sleep(60)  # Обновление цен и отсылка уведомлений каждые 60 секунд
    
