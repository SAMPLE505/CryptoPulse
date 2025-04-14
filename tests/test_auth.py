#from unittest.mock import patch
from tests.conftest import test_client

# Тест успешной регистрации пользователя
def test_user_registration_success(test_client):
    user_data = {
        "email": "test@example.com",
        "password": "securepassword",
        "username": "Test User"
    }
    
    response = test_client.post("/auth/register", json=user_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "User successfully registered"
    assert "id" in response_data["user"]
    assert response_data["user"]["email"] == user_data["email"]
    assert response_data["user"]["username"] == user_data["username"]


# Тест регистрации существующего пользователя
def test_user_registration_existing_user(test_client):
    user_registration_data = {
        "email": "test@example.com",
        "password": "securepassword",
        "username": "Test User"
    }
    
    # Создание пользователя
    test_client.post("/auth/register", json=user_registration_data)
    
    # Попытка зарегистрировать того же пользователя снова
    response = test_client.post("/auth/register", json=user_registration_data)
    
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "User already exists"


# Тест удачного входа пользователя
def test_user_login_success(test_client):

    user_registration_data = {
        "email": "test@example.com",
        "password": "securepassword",
        "username": "Test User"
    }

    user_login_data = {
        "email": "test@example.com",
        "password": "securepassword",
    }

    response = test_client.post("/auth/register", json=user_registration_data)
    assert response.status_code == 200

    response = test_client.post("/auth/login", json=user_login_data)
    assert response.status_code == 200
    assert "access" in response.json()


# Тест неудачного входа пользователя с невалидными данными
def test_user_login_invalid(test_client):

    user_registration_data = {
        "email": "test@example.com",
        "password": "securepassword",
    }

    response = test_client.post("/auth/login", json=user_registration_data)
    assert response.status_code == 400
    assert "detail" in response.json()
