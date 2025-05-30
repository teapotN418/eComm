from fastapi import APIRouter, Request
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from contextlib import asynccontextmanager
from fastapi import UploadFile, File, Form
from typing import Annotated

from src.app.services.async_minio import MinioServerAsync
from src.app.api.deps import get_minio_service

router = APIRouter()

@router.post('/upload/file',
    tags=["no-auth"],
)
async def upload_file(
    file: UploadFile,
    minio_handler: MinioServerAsync = Depends(get_minio_service),
):
    try:
        file_id = await minio_handler.upload_file(file.file, file.size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    return {"file_id": file_id}

@router.post("/upload/link",
    tags=["no-auth"],
)
async def upload_by_link(
    file_path: str,
    minio_handler: MinioServerAsync = Depends(get_minio_service),
):
    try:
        file_id = await minio_handler.upload_by_link(file_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    return {"file_id": file_id}

@router.get("/get-url/{object_id}",
    tags=["no-auth"],
)
async def get_picture_url(
    object_id: str,
    minio_handler: MinioServerAsync = Depends(get_minio_service),
):
    try:
        url = await minio_handler.get_object_url(object_id)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")