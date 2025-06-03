from fastapi import FastAPI, Request
import time
from src.routers.products import router as products_router
from src.routers.providers import router as providers_router
from src.routers.categories import router as categories_router
from src.monitoring import log_request, get_metrics

openapi_tags = [
    {"name": "unauthorized", "description": "Operations for everyone"},
    {"name": "admin", "description": "Operations for admin only"},
    {"name": "service", "description": "Service endpoints"}
]

app = FastAPI(
    openapi_tags=openapi_tags,
    docs_url='/products_docs',
    openapi_url='/products_openapi.json'
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


app.include_router(products_router, prefix='/products')
app.include_router(providers_router, prefix='/providers')
app.include_router(categories_router, prefix='/categories')
