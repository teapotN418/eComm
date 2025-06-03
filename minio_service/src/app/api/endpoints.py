from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile

from src.app.services.async_minio import MinioServerAsync
from src.app.api.deps import get_minio_service
from src.app.core.monitoring import log_file_operation
from src.app.api.deps import require_admin

router = APIRouter()


@router.post(
    '/upload/file',
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def upload_file(
    file: UploadFile,
    minio_handler: MinioServerAsync = Depends(get_minio_service),
):
    log_file_operation("upload_attempt", {
        "file_name": file.filename,
        "content_type": file.content_type,
        "size": file.size
    })

    allowed_types = ["image/", "video/"]
    allowed = False
    for type in allowed_types:
        if type in file.content_type:
            allowed = True
            break
    if not allowed:
        log_file_operation("upload_rejected", {
            "file_name": file.filename,
            "content_type": file.content_type,
            "reason": "file_type_not_allowed"
        })
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed."
        )
    try:
        file_id = await minio_handler.upload_file(file.file, file.size)
        log_file_operation("upload_success", {
            "file_name": file.filename,
            "file_id": file_id
        })
    except Exception as e:
        log_file_operation("upload_error", {
            "file_name": file.filename,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    return {"file_id": file_id}


@router.get(
    "/get-url/{object_id}",
    tags=["unauthorized"]
)
async def get_picture_url(
    object_id: str,
    minio_handler: MinioServerAsync = Depends(get_minio_service),
):
    log_file_operation("get_url_attempt", {
        "object_id": object_id
    })

    try:
        await minio_handler.check_exist(object_id)
    except Exception as e:
        log_file_operation("get_url_error", {
            "object_id": object_id,
            "error": str(e),
            "reason": "object_not_found"
        })
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")
    try:
        url = await minio_handler.get_object_url(object_id)
        log_file_operation("get_url_success", {
            "object_id": object_id
        })
    except Exception as e:
        log_file_operation("get_url_error", {
            "object_id": object_id,
            "error": str(e),
            "reason": "url_generation_failed"
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    return {"url": url}
