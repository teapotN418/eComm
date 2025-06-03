from fastapi import FastAPI, Request, Response
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

import src.app.api.endpoints as endpoints
from src.app.core.config import settings
from src.app.core.monitoring import log_request

tags_metadata = [
    {"name": "unauthorized", "description": "Operations for everyone"},
    {"name": "admin", "description": "Operations for admin only"},
    {"name": "service", "description": "Service endpoints"}
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/minio_docs",
    openapi_url='/minio_openapi.json'
)


@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time
    log_request(request, response_time, response.status_code)
    return response


@app.get("/metrics", tags=['service'])
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(endpoints.router, prefix="/files")
