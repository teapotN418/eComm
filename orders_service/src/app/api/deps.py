from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.app.db.setup import async_session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session