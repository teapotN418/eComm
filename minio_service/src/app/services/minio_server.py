from minio import Minio
import os
from dotenv import load_dotenv
from datetime import timedelta
import uuid

load_dotenv()


class MinioServer():
    __bucket_name: str

    def __init__(self, bucket_name):
        self.__minio_client = Minio(
            os.getenv('MINIO_ENDPOINT'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=True
        )
        self.__bucket_name = bucket_name

        found = self.__minio_client.bucket_exists(self.__bucket_name)
        if not found:
            self.__minio_client.make_bucket(self.__bucket_name)

    def put_picture(self, source_path: str) -> str | None:
        try:
            file_id = str(uuid.uuid4()) + '.jpg'

            self.__minio_client.fput_object(
                self.__bucket_name, file_id, source_path
            )
            return file_id
        except Exception:
            return None

    def get_object_url(self, object_id: str) -> str:
        return self.__minio_client.presigned_get_object(
            self.__bucket_name, object_id, expires=timedelta(hours=3))
