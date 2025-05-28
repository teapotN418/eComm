import pytest
from httpx import AsyncClient
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncTransaction, AsyncConnection, AsyncSession, create_async_engine

from src.app.core.config import settings
from src.app.core.security import security_config
from src.app.api.deps import get_db
from src.app.main import app

backend_url = "http://localhost:" + settings.BACKEND_PORT

db_url = settings.DATABASE_URL

pytestmark = pytest.mark.anyio

engine = create_async_engine(db_url)

# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection
        
@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction

@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield async_session

    await transaction.rollback()

@pytest.fixture()
async def client(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session
    
    app.dependency_overrides[get_db] = override_get_async_session
    yield AsyncClient(app=app, base_url=backend_url)
    del app.dependency_overrides[get_db]

    await transaction.rollback()

@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()