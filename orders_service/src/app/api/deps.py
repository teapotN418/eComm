from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from fastapi import Header, HTTPException, Depends, status

from src.app.db.setup import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_current_user_id(x_user_id: str = Header(None)):
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return int(x_user_id)


async def require_authenticated_user(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Forbidden: user_id mismatch")


async def require_admin(x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
