from .conftest import AsyncClient, Cookies, json, settings
import pytest
from fastapi import status

@pytest.fixture()
async def test_order_data():
    return {"pr": [{"id": 100, "q": 5}, {"id": 200, "q": 30}]}

@pytest.fixture()
async def client_with_order(client: AsyncClient, test_order_data: dict):
    cookies = Cookies()
    cookies.set(settings.CART_COOKIE_LOCATION, json.dumps(test_order_data))
    client.cookies=cookies
    yield client

@pytest.fixture()
def user_headers():
    return {"x-user-id": "50", "x-user-role": "user"}

@pytest.fixture()
def admin_headers():
    return {"x-user-id": "1", "x-user-role": "admin"}

async def test_create_get_order(client_with_order, user_headers):

    response = await client_with_order.get("/orders/user", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = await client_with_order.post("/orders/user", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    order = response.json()
    
    response = await client_with_order.get("/orders/user", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == order["id"]

async def test_admin_order_operations(client_with_order, user_headers, admin_headers):
    user_id = 50
    
    response = await client_with_order.post("/orders/user", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    order_id = response.json()["id"]

    response = await client_with_order.get("/orders", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

    response = await client_with_order.get(f"/orders/user/{user_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

    response = await client_with_order.get(f"/orders/order/{order_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK

    new_status = "approved"
    response = await client_with_order.put(
        f"/orders/order/{order_id}",
        params={"order_status": new_status},
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == new_status

    response = await client_with_order.delete(f"/orders/order/{order_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK

    response = await client_with_order.get(f"/orders/order/{order_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_bad_order(client, user_headers):
    response = await client.post("/orders/user", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

async def test_unauthorized_access(client_with_order, user_headers):
    user_id = 50
    other_user_id = 51
    
    response = await client_with_order.post("/orders/user", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    order_id = response.json()["id"]

    bad_headers = {"x-user-id": str(other_user_id), "x-user-role": "user"}
    response = await client_with_order.get(f"/orders/user/{user_id}", headers=bad_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = await client_with_order.get("/orders", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = await client_with_order.put(
        f"/orders/order/{order_id}",
        params={"order_status": "approved"},
        headers=user_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN