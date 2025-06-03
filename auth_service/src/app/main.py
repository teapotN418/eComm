from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import time

import src.app.api.endpoints as endpoints
from src.app.core.config import settings
from src.app.core.monitoring import log_request, get_metrics

tags_metadata = [
    {"name": "unauthorized", "description": "Operations for everyone"},
    {"name": "authorized", "description": "Operations for authorized users only"},
    {"name": "service", "description": "Service endpoints"}
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/auth_docs",
    openapi_url='/auth_openapi.json'
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
    return get_metrics()

app.include_router(endpoints.router, prefix="/auth")
