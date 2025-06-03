from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from fastapi import Header, HTTPException, status

from src.app.db.setup import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def require_admin(
    x_user_id: str = Header(...),
    x_user_role: str = Header(...),
):
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return {"id": int(x_user_id), "role": x_user_role}


async def get_current_user(
    x_user_id: str = Header(...),
    x_user_role: str = Header(...),
):
    return {"id": int(x_user_id), "role": x_user_role}
