from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from src.config import config
from src.router import router
from src.middleware import LoggingMiddleware

openapi_tags = [
    {'name': 'unauthorized', 'description': 'Does not require authorization'},
    {'name': 'authorized', 'description': 'Requires proper authorization'}
]

app = FastAPI(
    openapi_tags=openapi_tags,
    docs_url='/docs'
)

# Добавляем middleware для логирования
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.GATEWAY_URL],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['*']
)

# Добавляем эндпоинт для метрик Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router, prefix='/api/reviews')
