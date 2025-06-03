from .conftest import AsyncClient
import pytest

@pytest.fixture()
async def test_user_data():
    return {
        "email": "21ov7f6g@mail.ru",
        "password": "12345"
    }

@pytest.fixture()
async def register_user(client: AsyncClient, test_user_data: dict):
    response = await client.post(
        "/users/register",
        json=test_user_data,
    )
    assert response.status_code == 200
    return response

async def test_create_user(register_user, test_user_data):
    assert register_user.json()["email"] == test_user_data["email"]
    assert register_user.json()["role"] == "user"

async def test_user_id(client, register_user):
    user_id = register_user.json()["id"]

    response = await client.get(f"/users/profile/{user_id}")
    assert response.status_code == 200
    assert response.json() == register_user.json()

    new_password = "123456"
    bad_password="123"
    
    response = await client.put(f"/users/profile/{user_id}", json={"password": bad_password})
    assert response.status_code == 422

    response = await client.put(f"/users/profile/{user_id}", json={"password": new_password})
    assert response.status_code == 200

    response = await client.delete(f"/users/profile/{user_id}")
    assert response.status_code == 200

    response = await client.get(f"/users/profile/{user_id}")
    assert response.status_code == 404

    response = await client.put(f"/users/profile/{user_id}", json={"password": new_password})
    assert response.status_code == 404

    response = await client.delete(f"/users/profile/{user_id}")
    assert response.status_code == 404

async def test_admin_id(client, register_user):
    user_id = register_user.json()["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == register_user.json()

    new_password = "123456"
    bad_password="123"
    
    response = await client.put(f"/users/{user_id}", json={"password": bad_password})
    assert response.status_code == 422

    response = await client.put(f"/users/{user_id}", json={"password": new_password})
    assert response.status_code == 200

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 404

    response = await client.put(f"/users/{user_id}", json={"password": new_password})
    assert response.status_code == 404

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 404

async def test_admin_users(client, register_user, test_user_data):
    test_data = test_user_data
    test_data["role"] = "user"

    response = await client.post("/users", json=test_data)
    assert response.status_code == 409

    test_data["email"] = "3h4gv0hrg3wri@mail.ru"
    response = await client.post("/users", json=test_data)
    assert response.status_code == 200

    users_list = await client.get("/users")
    assert response.json() in users_list.json()
    assert register_user.json() in users_list.json()