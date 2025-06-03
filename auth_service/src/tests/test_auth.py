from .conftest import security_config, AsyncClient
import pytest

@pytest.fixture()
async def test_user_data():
    return {
        "email": "test_user@mail.ru",
        "password": "12345"
    }

@pytest.fixture()
async def test_admin_data():
    return {
        "email": "test_admin@mail.ru",
        "password": "12345"
    }

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
        json={"email": "p12fh39b82f@mail.ru", "password": "130mfn23f"}
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
    response = await authed_client.get(
        "/auth/verify"
    )
    assert response.status_code == 200

async def test_verify_admin(authed_admin):
    response = await authed_admin.get(
        "/auth/verify"
    )
    assert response.status_code == 200

async def test_wrong_verify(client):
    response = await client.get(
        "/auth/verify"
    )
    assert response.status_code == 401

async def test_logout(authed_client):
    response = await authed_client.post(
        "/auth/logout"
    )
    assert response.status_code==200
    authed_client.cookies = response.cookies
    assert not security_config.JWT_ACCESS_COOKIE_NAME in authed_client.cookies
    assert not security_config.JWT_REFRESH_COOKIE_NAME in authed_client.cookies