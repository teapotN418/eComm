from typing import AsyncGenerator
from src.app.services.async_minio import MinioServerAsync

async def get_minio_service() -> AsyncGenerator[MinioServerAsync, None]:
    minio_handler = MinioServerAsync()
    await minio_handler.initialize()
    try:
        yield minio_handler
    finally:
        await minio_handler.close()