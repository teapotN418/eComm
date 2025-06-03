from fastapi import FastAPI, Request

import src.app.api.endpoints.cart as cart
import src.app.api.endpoints.orders as orders
from src.app.core.config import settings
from src.app.core.monitoring import log_request, get_metrics
import time


tags_metadata = [
    {"name": "unauthorized", "description": "Operations for everyone"},
    {"name": "authorized", "description": "Operations for authorized users only"},
    {"name": "admin", "description": "Operations for admin only"},
    {"name": "service", "description": "Service endpoints"}
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url='/orders_docs',
    openapi_url='/orders_openapi.json'
)


app.include_router(cart.router, prefix="/cart")
app.include_router(orders.router, prefix="/orders")


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
