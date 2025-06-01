from .conftest import security_config, AsyncClient
import pytest

@pytest.fixture()
async def test_user_data():
    return {
        "email": "user@mail.ru",
        "password": "12345"
    }

@pytest.fixture()
async def test_admin_data():
    return {
        "email": "admin@mail.ru",
        "password": "12345"
    }

# Для тестов требуется чтобы оба пользователя сверху были в БД

@pytest.fixture()
async def authed_client(client: AsyncClient, test_user_data: dict):
    response = await client.post(
        "/auth/login",
        json=test_user_data,
    )
    assert response.status_code == 200
    
    cookies = dict(response.cookies)
    client.cookies=cookies
    yield client

@pytest.fixture()
async def authed_admin(client: AsyncClient, test_admin_data: dict):
    response = await client.post(
        "/auth/login",
        json=test_admin_data,
    )
    assert response.status_code == 200
    
    cookies = dict(response.cookies)
    client.cookies=cookies
    yield client

async def test_cookies(authed_client):
    assert security_config.JWT_ACCESS_COOKIE_NAME in authed_client.cookies
    assert security_config.JWT_REFRESH_COOKIE_NAME in authed_client.cookies

async def test_wrong_login(client):
    response = await client.post(
        "/auth/login",
        json={"email": "123@mail.ru", "password": "abcder"}
    )
    assert response.status_code == 401

async def test_refresh(authed_client):
    response = await authed_client.post(
        "/auth/refresh"
    )
    assert response.status_code == 200

async def test_wrong_refresh(client):
    response = await client.post(
        "/auth/refresh"
    )
    assert response.status_code == 401

async def test_verify_user(authed_client):
    response = await authed_client.post(
        "/auth/verify"
    )
    assert response.status_code == 200
    assert response.json()["role"] == "user"

async def test_verify_admin(authed_admin):
    response = await authed_admin.post(
        "/auth/verify"
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"

async def test_wrong_verify(client):
    response = await client.post(
        "/auth/verify"
    )
    assert response.status_code == 401

async def test_role_verify_user(authed_client):
    response = await authed_client.post(
        "/auth/verify-role?role=user"
    )
    assert response.status_code == 200
    response = await authed_client.post(
        "/auth/verify-role?role=admin"
    )
    assert response.status_code == 403

async def test_role_verify_admin(authed_admin):
    response = await authed_admin.post(
        "/auth/verify-role?role=admin"
    )
    assert response.status_code == 200

async def test_wrong_role_verify(client):
    response = await client.post(
        "/auth/verify-role?role=user"
    )
    assert response.status_code == 401

async def test_logout(authed_client):
    response = await authed_client.post(
        "/auth/logout"
    )
    authed_client.cookies = response.cookies
    assert not security_config.JWT_ACCESS_COOKIE_NAME in authed_client.cookies
    assert not security_config.JWT_REFRESH_COOKIE_NAME in authed_client.cookies