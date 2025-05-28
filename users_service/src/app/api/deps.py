from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.app.core.security import security_obj
from src.app.db.setup import async_session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

async def set_response_state(request: Request, payload):
    request.state.sub = payload.sub
    request.state.data = payload.model_dump(include="role")

async def require_access(request: Request):
    try:
        payload = await security_obj.access_token_required(request)
        await set_response_state(request, payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )
    
async def require_fresh_access(request: Request):
    try:
        payload = await security_obj.fresh_token_required(request)
        await set_response_state(request, payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

async def require_refresh(request: Request):
    try:
        payload = await security_obj.refresh_token_required(request)
        await set_response_state(request, payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

def require_role(required_role: str, fresh: bool = False):
    async def role_checker(request: Request):
        if fresh:
            await require_fresh_access(request)
        else:
            await require_access(request)
        if request.state.data.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Require {required_role} role",
            )
    return role_checker