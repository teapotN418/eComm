from .conftest import AsyncClient, Cookies, json, settings
import pytest

@pytest.fixture()
async def test_order_data():
    return {"pr": [{"id": 100, "q": 5}, {"id": 200, "q": 30}]}

@pytest.fixture()
async def client_with_order(client: AsyncClient, test_order_data: dict):
    cookies = Cookies()
    cookies.set(settings.CART_COOKIE_LOCATION, json.dumps(test_order_data))
    client.cookies=cookies
    yield client

async def test_create_get_order(client_with_order):
    user_id = 50

    response = await client_with_order.get(f"/orders/user/me/{user_id}")
    assert response.status_code == 200
    assert response.json() == []

    response = await client_with_order.get(f"/orders/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == []

    response = await client_with_order.get(f"/orders")
    assert response.status_code == 200
    assert response.json() == []

    response = await client_with_order.post(f"/orders/user/{user_id}")
    assert response.status_code == 200

    response = await client_with_order.get(f"/orders/user/me/{user_id}")
    assert response.status_code == 200
    assert response.json() != []

    response = await client_with_order.get(f"/orders/user/{user_id}")
    assert response.status_code == 200
    assert response.json() != []

    response = await client_with_order.get(f"/orders")
    assert response.status_code == 200
    assert response.json() != []

async def test_order_id(client_with_order):
    user_id = 50
    status = "approved"
    
    response = await client_with_order.post(f"/orders/user/{user_id}")
    assert response.status_code == 200
    order_id = response.json()["id"]
    order_json = response.json()

    response = await client_with_order.get(f"/orders/order/{order_id}")
    assert response.status_code == 200
    assert response.json()["items"] == order_json["items"]

    response = await client_with_order.put(f"/orders/order/{order_id}?order_status={status}")
    assert response.status_code == 200
    assert response.json()["status"] == status

    response = await client_with_order.put(f"/orders/order/{order_id}?order_status=wqefqe")
    assert response.status_code == 422

    response = await client_with_order.delete(f"/orders/order/{order_id}")
    assert response.status_code == 200

    response = await client_with_order.get(f"/orders/order/{order_id}")
    assert response.status_code == 404

    response = await client_with_order.put(f"/orders/order/{order_id}?order_status={status}")
    assert response.status_code == 404

    response = await client_with_order.delete(f"/orders/order/{order_id}")
    assert response.status_code == 404

async def test_bad_order(client):
    user_id = 50
    
    response = await client.post(f"/orders/user/{user_id}")
    assert response.status_code == 400