from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionUpdateSchema
from uuid import UUID, uuid4


# Функция добавления новой подписки
def add_user_subscription(user_id: UUID, symbol: str, threshold: float, above: bool, db: Session) -> Subscription:
    subscription = Subscription(
        user_id=user_id,
        symbol=symbol,
        threshold=threshold,
        above=above
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


# Функция получения всех подписок пользователя
def get_user_subscriptions(user_id: UUID, db: Session) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()


# Функция получения выбранной подписки пользователя
def get_user_subscription(subscription_id: UUID, user_id: UUID, db: Session) -> Subscription:
    return db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user_id
    ).first()


# Функция обновления подписки
def update_user_subscription(subscription: Subscription, updates: SubscriptionUpdateSchema, db: Session) -> Subscription:
    setattr(subscription, "threshold", updates.threshold)
    setattr(subscription, "above", updates.above)
    db.commit()
    db.refresh(subscription)
    return subscription


# Функция удаления подписки из БД
def delete_user_subscription(subscription: Subscription, db: Session):
    db.delete(subscription)
    db.commit()


# Функция активации/деактивации подписки
def toggle_user_subscription(subscription: Subscription, db: Session):
    is_active = not subscription.is_active
    setattr(subscription, "is_active", is_active)
    db.commit()
    db.refresh(subscription)
    return subscription