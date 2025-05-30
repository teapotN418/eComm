from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import src.app.api.endpoints as endpoints
from src.app.core.config import settings
from src.app.services.async_minio import MinioServerAsync


tags_metadata = [
    {"name": "no-auth", "description": "Operations for everyone"},
]

origins = [
    "*",
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/files")