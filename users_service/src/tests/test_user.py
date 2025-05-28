from .conftest import security_config, AsyncClient
import pytest

@pytest.fixture()
async def test_user_data():
    return {
        "email": "test_reg@mail.com",
        "password": "12345"
    }

@pytest.fixture()
async def register_user(client: AsyncClient, test_user_data: dict):
    response = await client.post(
        "/users/register",
        json=test_user_data,
    )
    assert response.status_code == 200
    return response.json()

@pytest.fixture()
async def authenticated_client(client: AsyncClient, test_user_data: dict, register_user):
    response = await client.post(
        "/users/auth/login",
        json=test_user_data,
    )
    assert response.status_code == 200
    
    cookies = dict(response.cookies)
    client.cookies=cookies
    yield client

async def test_create_user(register_user):
    assert register_user["email"] == "test_reg@mail.com"
    assert register_user["role"] == "user"

async def test_wrong_login(client, register_user):
    response = await client.post(
        "/users/auth/login",
        json={"email": "123@mail.ru", "password": "abcder"}
    )
    assert response.status_code == 401

async def test_login_user(authenticated_client):
    assert security_config.JWT_ACCESS_COOKIE_NAME in authenticated_client.cookies
    assert security_config.JWT_REFRESH_COOKIE_NAME in authenticated_client.cookies
    
    response = await authenticated_client.get("/users/me")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "test_reg@mail.com"

async def test_token_actions(authenticated_client):
    response = await authenticated_client.post("/users/auth/refresh")
    assert response.status_code == 200
    response = await authenticated_client.post("/users/auth/logout")
    assert response.status_code == 200

async def test_change_user(authenticated_client, test_user_data):
    new_password = "123456"
    bad_password="123"
    
    response = await authenticated_client.put("/users/me", json={"password": bad_password})
    assert response.status_code == 422

    response = await authenticated_client.put("/users/me", json={"password": new_password})
    assert response.status_code == 200
    
    response = await authenticated_client.post("/users/auth/login", json=test_user_data)
    assert response.status_code == 401
    
    changed_data = test_user_data
    changed_data["password"] = new_password

    response = await authenticated_client.post("/users/auth/login", json=changed_data)
    assert response.status_code == 200

async def test_delete_user(authenticated_client):
    response = await authenticated_client.delete("/users/me")
    assert response.status_code == 200
    assert not security_config.JWT_ACCESS_COOKIE_NAME in response.cookies
    assert not security_config.JWT_REFRESH_COOKIE_NAME in response.cookies

async def test_forbidden_user(authenticated_client):
    response = await authenticated_client.get("/users")
    assert response.status_code == 403