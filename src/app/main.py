from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import src.app.api.endpoints as endpoints
from src.app.core.config import settings

tags_metadata = [
    {"name": "no-auth", "description": "Operations for everyone"},
    {"name": "authenticated", "description": "Operations for all authenticated"},
    {"name": "admin", "description": "Operations for admins only"},
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

app.include_router(endpoints.router, prefix="/users")