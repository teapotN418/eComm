from fastapi import FastAPI
from prometheus_client import make_asgi_app
from src.router import router
from src.middleware import LoggingMiddleware

openapi_tags = [
    {"name": "unauthorized", "description": "Operations for everyone"},
    {"name": "authorized", "description": "Operations for authorized users only"},
    {"name": "service", "description": "Service endpoints"}
]

app = FastAPI(
    openapi_tags=openapi_tags,
    docs_url='/reviews_docs',
    openapi_url='/reviews_openapi.json'
)

# Добавляем middleware для логирования
app.add_middleware(LoggingMiddleware)

# Добавляем эндпоинт для метрик Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router, prefix='/reviews')
