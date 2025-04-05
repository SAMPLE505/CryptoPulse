from tests.conftest import test_client

# Тест на регистрацию пользователя
def test_get_coin_price(test_client):

    # Тест на стандартное поведение эндпоинта
    response = test_client.get("/crypto/price", params={"BTC"})
    assert response.status_code == 200
    """
    assert response_data["message"] == "User successfully registered"
    assert response_data["user"]["email"] == user_data["email"]
    assert response_data["user"]["full_name"] == user_data["full_name"]
    assert "id" in response_data["user"]

    # Тест случая, когда пользователь уже существует
    response = test_client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "User already exists"
    """
