from miniopy_async import Minio
from datetime import timedelta
import uuid
from typing import BinaryIO

from src.app.core.config import settings

class MinioServerAsync():
    __bucket_name: str

    def __init__(self):
        self.__minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=True
        )
        self.__bucket_name = settings.MINIO_BUCKET

    async def initialize(self):
        found = await self.__minio_client.bucket_exists(self.__bucket_name)
        if not found:
            await self.__minio_client.make_bucket(self.__bucket_name)

    async def upload_file(self, file: BinaryIO, length: int):
        try:
            file_id = str(uuid.uuid4()) + '.jpg'
            await self.__minio_client.put_object(self.__bucket_name, file_id, file, length)
        except Exception as e:
            raise e
        return file_id

    async def upload_by_link(self, source_path: str) -> str:
        try:
            file_id = str(uuid.uuid4()) + '.jpg'
            await self.__minio_client.fput_object(
                self.__bucket_name, file_id, source_path
            )
        except Exception as e:
            raise e
        return file_id
    
    async def get_object_url(self, object_id: str) -> str:
        try:
            link = await self.__minio_client.presigned_get_object(
                self.__bucket_name, object_id, expires=timedelta(hours=3)
            )
        except Exception as e:
            raise e
        return link