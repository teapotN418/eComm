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

@pytest.fixture()
async def test_user_headers(register_user):
    user_data = register_user.json()
    return {
        "x-user-id": str(user_data["id"]),
        "x-user-role": user_data["role"]
    }

@pytest.fixture()
async def test_admin_headers():
    return {
        "x-user-id": "999",
        "x-user-role": "admin"
    }

async def test_create_user(register_user, test_user_data):
    assert register_user.json()["email"] == test_user_data["email"]
    assert register_user.json()["role"] == "user"


async def test_user_id(client, register_user, test_user_headers):
    
    response = await client.get(
        f"/users/profile",
        headers=test_user_headers
    )
    assert response.status_code == 200
    assert response.json() == register_user.json()

    new_password = "123456"
    bad_password = "123"
    
    response = await client.put(
        f"/users/profile",
        json={"password": bad_password},
        headers=test_user_headers
    )
    assert response.status_code == 422

    response = await client.put(
        f"/users/profile",
        json={"password": new_password},
        headers=test_user_headers
    )
    assert response.status_code == 200

    response = await client.delete(
        f"/users/profile",
        headers=test_user_headers
    )
    assert response.status_code == 200

    response = await client.get(
        f"/users/profile",
        headers=test_user_headers
    )
    assert response.status_code == 404

    response = await client.put(
        f"/users/profile",
        json={"password": new_password},
        headers=test_user_headers
    )
    assert response.status_code == 404

    response = await client.put(
        f"/users/profile",
        json={"password": new_password},
        headers=test_user_headers
    )
    assert response.status_code == 404

async def test_admin_id(client, register_user, test_admin_headers):
    user_id = register_user.json()["id"]
    
    response = await client.get(
        f"/users/{user_id}",
        headers=test_admin_headers
    )
    assert response.status_code == 200
    assert response.json() == register_user.json()

    response = await client.put(
        f"/users/{user_id}",
        json={"password": "new_admin_password"},
        headers=test_admin_headers
    )
    assert response.status_code == 200

    response = await client.delete(
        f"/users/{user_id}",
        headers=test_admin_headers
    )
    assert response.status_code == 200

    response = await client.get(
        f"/users/{user_id}",
        headers=test_admin_headers
    )
    assert response.status_code == 404

    response = await client.put(
        f"/users/{user_id}",
        json={"password": "new_admin_password"},
        headers=test_admin_headers
    )
    assert response.status_code == 404

    response = await client.put(
        f"/users/{user_id}",
        json={"password": "new_admin_password"},
        headers=test_admin_headers
    )
    assert response.status_code == 404


async def test_admin_users(client, test_user_data, test_admin_headers):
    response = await client.post(
        "/users",
        json=test_user_data,
        headers=test_admin_headers
    )
    assert response.status_code == 200

    users_list = await client.get(
        "/users",
        headers=test_admin_headers
    )
    assert response.json() in users_list.json()

    response = await client.post(
        "/users",
        json=test_user_data,
        headers=test_admin_headers
    )
    assert response.status_code == 409



async def test_no_access(client, register_user):
    user_id = register_user.json()["id"]
    
    response = await client.get(f"/users/profile")
    assert response.status_code == 422

    fake_headers = {
        "x-user-id": str(user_id),
        "x-user-role": "user"
    }
    response = await client.get(
        "/users",
        headers=fake_headers
    )
    assert response.status_code == 403

    other_user_headers = {
        "x-user-id": "-1",
        "x-user-role": "user"
    }
    response = await client.get(
        f"/users/profile",
        headers=other_user_headers
    )
    assert response.status_code == 404