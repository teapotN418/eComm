from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import time
from src.config import config
from src.routers.products import router as products_router
from src.routers.providers import router as providers_router
from src.routers.categories import router as categories_router
from src.monitoring import log_request, get_metrics

openapi_tags = [
    {'name': 'unauthorized', 'description': 'Does not require authorization'},
    {'name': 'authorized', 'description': 'Requires proper authorization'}
]

app = FastAPI(
    openapi_tags=openapi_tags,
    docs_url='/docs'
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
    allow_origins=[config.GATEWAY_URL],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['*']
)

app.include_router(products_router, prefix='/api/products')
app.include_router(providers_router, prefix='/api/providers')
app.include_router(categories_router, prefix='/api/categories')
