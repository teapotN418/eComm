from fastapi import HTTPException, status, Request
from functools import lru_cache

from src.app.services.async_minio import MinioServerAsync

async def get_minio_service() -> MinioServerAsync:
    minio_handler = MinioServerAsync()
    await minio_handler.initialize()
    return minio_handler