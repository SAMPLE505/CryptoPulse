# 📘 CryptoPulse

Этот проект предоставляет API для:
- 🧑‍💻 Регистрации и входа пользователей
- 📈 Получения курса криптовалют
- 📋 Получения списка криптовалют

---

## 🚀 Запуск проекта

### 1. Установка зависимостей с помощью Poetry

Создайте виртуальное окружение с помощью venv:

```bash
python -m venv venv
```
Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями и окружением. Установите его:

```bash
pip install poetry
```

Затем установите зависимости:

```bash
poetry install
```

---

### 2. Запуск сервисов через Docker Compose

Для работы проекта необходимы PostgreSQL и Redis. Они запускаются в контейнерах с помощью `docker-compose.yml`.

```bash
docker-compose up -d
```

После этого можно запустить FastAPI-приложение:

```bash
uvicorn app.main:app --reload
```

---

### 3. Переменные окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```
# Корень проекта
PYTHONPATH = .

# Безопасность
SECRET_KEY = "YOUR SECRET KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_MINUTES = 30
REFRESH_TOKEN_TTL_DAYS = 30

# База данных
DATABASE_URL = "postgresql://test_user:test_password@localhost:5433/test_db"

# Redis
REDIS_HOST = "localhost"
REDIS_DB = 0
REDIS_PORT = 6380

# Ключ API CoinMarketCap
API_KEY = "YOUR CoinMarketCapKey"

# Время жизни данных о криптовалюте в Redis
CRYPTO_PRICE_TTL_SECONDS = 60
CRYPTO_LIST_TTL_MINUTES = 60
```

---

## 🧪 Тестирование

Для запуска тестовой среды используйте:

```bash
docker-compose -f docker-compose.test.yml up -d
```

> Это поднимет отдельные контейнеры PostgreSQL и Redis, используемые только для автотестов.

Запуск тестов:

```bash
pytest
```

---

## 🔐 Аутентификация

### POST `/auth/register`

Регистрирует нового пользователя.

#### Request:
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Response:
```json
{
  "message": "User successfully registered",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

---

### POST `/auth/login`

Аутентифицирует пользователя и возвращает access-токен. Также устанавливает refresh-токен в `HttpOnly`-cookie.

#### Request:
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Response:
```json
{
  "access": "jwt_access_token",
  "token_type": "bearer",
  "expires_in": 900
}
```

> `refresh_token` устанавливается в cookie и используется для обновления access-токена.

---

## 💰 Криптовалюта

### GET `/crypto/price?symbol=BTC`

Возвращает текущую цену указанной криптовалюты по символу.

#### Query Parameters:
- `symbol` — тикер монеты (например, `BTC`, `ETH`, `USDT`)

#### Response:
```json
{
  "symbol": "BTC",
  "price": 67000.00
}
```

#### Возможные ошибки:
- `404 Not Found`: Монета не найдена
- `504 Gateway Timeout`: CoinMarketCap API не ответил вовремя
- `502 Bad Gateway`: Ошибка при обращении к CoinMarketCap API
- `500 Internal Server Error`: Непредвиденная ошибка

---

### GET `/crypto/list`

Возвращает список всех доступных криптовалют.

#### Response:
```json
{
  "data": [
    {
      "symbol": "BTC",
      "name": "Bitcoin"
    },
    {
      "symbol": "ETH",
      "name": "Ethereum"
    }
  ]
}
```

#### Возможные ошибки:
- `504 Gateway Timeout`: CoinMarketCap API не ответил вовремя
- `502 Bad Gateway`: Ошибка при обращении к CoinMarketCap API
- `500 Internal Server Error`: Непредвиденная ошибка

---

## 🛠️ Используемые технологии

- **FastAPI** — backend-фреймворк
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных (в контейнере через `docker-compose.yml`)
- **Redis** — хранение refresh-токенов (в контейнере через `docker-compose.yml`)
- **Poetry** — управление зависимостями и окружением
- **JWT** — авторизация
- **httpx** — асинхронные HTTP-запросы
- **CoinMarketCap API** — данные по криптовалютам
- **Docker / Docker Compose** — контейнеризация окружения

---

## 📁 Структура проекта

```
app/
├── core/              # Безопасность, конфиги
├── models/            # SQLAlchemy модели
├── schemas/           # Pydantic-схемы
├── services/          # Логика работы с криптой, пользователями и стороннеми задачами
├── api/               # Роутеры FastAPI
├── database.py        # Подключение к БД
├── exceptions.py      # Кастомные исключения
└── main.py            # Точка входа
```

---

## 📦 TODO

- Отслеживание курса валют с помощью подписок
- Обновление access-токена по refresh-токену
- Защита роутов авторизацией
- Тесты для Redis и токенов
- Документация Swagger (`/docs`)
