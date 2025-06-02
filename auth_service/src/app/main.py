from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import time

import src.app.api.endpoints as endpoints
from src.app.core.config import settings
from src.app.core.monitoring import log_request, get_metrics

tags_metadata = [
    {"name": "no-auth", "description": "Operations for everyone"},
    {"name": "authenticated", "description": "Operations for all authenticated"},
]

origins = [
    "*",
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs",
)

@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time
    log_request(request, response_time, response.status_code)
    return response

@app.get("/metrics")
async def metrics():
    return get_metrics()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/auth")