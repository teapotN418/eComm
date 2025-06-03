import pytest
from httpx import AsyncClient
import asyncio
from typing import AsyncGenerator

from src.app.main import app

backend_url = "http://localhost:8000"

pytestmark = pytest.mark.anyio

# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    yield AsyncClient(app=app, base_url=backend_url)

@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
