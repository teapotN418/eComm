from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile

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
    allowed_types = ["image/", "video/"]
    allowed = False
    for type in allowed_types:
        if type in file.content_type:
            allowed = True
            break
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"File type {file.content_type} not allowed."
        )
    try:
        file_id = await minio_handler.upload_file(file.file, file.size)
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
        await minio_handler.check_exist(object_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")
    try:
        url = await minio_handler.get_object_url(object_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    return {"url": url}