from miniopy_async import Minio
from datetime import timedelta
import uuid
from typing import BinaryIO

from src.app.core.config import settings


class MinioServerAsync():
    __minio_client: Minio
    __bucket_name: str

    def __init__(self):
        self.__minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        self.__bucket_name = settings.MINIO_BUCKET

    async def initialize(self):
        found = await self.__minio_client.bucket_exists(self.__bucket_name)
        if not found:
            await self.__minio_client.make_bucket(self.__bucket_name)

    async def close(self):
        await self.__minio_client.close_session()

    async def upload_file(self, file: BinaryIO, length: int):
        try:
            file_id = str(uuid.uuid4())
            await self.__minio_client.put_object(self.__bucket_name, file_id, file, length)
        except Exception as e:
            raise e
        return file_id

    async def check_exist(self, object_id: str) -> None:
        try:
            await self.__minio_client.stat_object(self.__bucket_name, object_id)
        except Exception as e:
            raise e

    async def get_object_url(self, object_id: str) -> str:
        try:
            link = await self.__minio_client.presigned_get_object(
                self.__bucket_name, object_id, expires=timedelta(hours=3)
            )
        except Exception as e:
            raise e
        return link
