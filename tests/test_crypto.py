from tests.conftest import test_client

# Тест успешного получения цены валюты
def test_get_coin_price_success(test_client):

    response = test_client.get("/crypto/price", params={"symbol": "BTC"})
    assert response.status_code == 200
    assert "price" in response.json()


# Тест получения цены несуществующей валюты
def test_get_coin_price_invalid(test_client):

    response = test_client.get("/crypto/price", params={"symbol": "SOMERANDOMCOIN"})
    assert response.status_code == 404
    assert "detail" in response.json()


# Тест успешного получения списка валют
def test_get_coins_list_success(test_client):

    response = test_client.get("/crypto/list")
    assert response.status_code == 200
    assert "data" in response.json()
