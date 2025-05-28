from .conftest import security_config, AsyncClient
import pytest

@pytest.fixture()
async def test_user_data():
    return {
        "email": "test_reg@mail.com",
        "password": "12345"
    }

@pytest.fixture()
async def register_admin(client: AsyncClient, test_user_data: dict):
    response = await client.post(
        "/users/admin",
        json=test_user_data,
    )
    assert response.status_code == 200
    return response.json()

@pytest.fixture()
async def admin_client(client: AsyncClient, test_user_data: dict, register_admin: dict):
    response = await client.post(
        "/users/auth/login",
        json=test_user_data,
    )
    assert response.status_code == 200
    
    cookies = dict(response.cookies)
    client.cookies=cookies
    yield client

async def test_get_users(admin_client):
    response = await admin_client.get("/users")
    assert response.status_code == 200

async def test_user_manipulations(admin_client, test_user_data):
    test_data = test_user_data
    test_data["role"] = "user"

    response = await admin_client.post("/users", json=test_data)
    assert response.status_code == 409

    test_data["email"] = "new@email.com"
    response = await admin_client.post("/users", json=test_data)
    assert response.status_code == 200

    id = response.json()["id"]

    response = await admin_client.get("/users/0")
    assert response.status_code == 404

    response = await admin_client.put("/users/0", json={"password": "123456"})
    assert response.status_code == 404

    response = await admin_client.delete("/users/0")
    assert response.status_code == 404
    

    response = await admin_client.get(f"/users/{id}")
    assert response.status_code == 200

    response = await admin_client.put(f"/users/{id}", json={"password": "123456"})
    assert response.status_code == 200
    
    response = await admin_client.delete(f"/users/{id}")
    assert response.status_code == 200

    response = await admin_client.get(f"/users/{id}")
    assert response.status_code == 404
