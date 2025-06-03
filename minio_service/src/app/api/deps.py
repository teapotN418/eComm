from typing import AsyncGenerator
from fastapi import Header, HTTPException, status
from src.app.services.async_minio import MinioServerAsync


async def get_minio_service() -> AsyncGenerator[MinioServerAsync, None]:
    minio_handler = MinioServerAsync()
    await minio_handler.initialize()
    try:
        yield minio_handler
    finally:
        await minio_handler.close()


async def require_admin(
    x_user_id: str = Header(...),
    x_user_role: str = Header(...),
):
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return {"id": int(x_user_id), "role": x_user_role}
