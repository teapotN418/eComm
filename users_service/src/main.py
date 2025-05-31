import os
import time
import json
import logging
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest

SERVICE_NAME = "users_service"

# Настройка логирования в stdout в формате JSON
logger = logging.getLogger("service_logger")
handler = logging.StreamHandler()
formatter = logging.Formatter(json.dumps({
    "time": "%(asctime)s",
    "level": "%(levelname)s",
    "service": SERVICE_NAME,
    "message": "%(message)s"
}))
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.setLevel(logging.INFO)

# Метрики Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["service", "method", "endpoint"]
)

app = FastAPI()

@app.middleware("http")
async def metrics_and_logging_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        logger.error(f"Exception: {e}")
        raise
    duration = time.time() - start_time

    # Метрики
    REQUEST_COUNT.labels(
        service=SERVICE_NAME,
        method=request.method,
        endpoint=request.url.path,
        status=status
    ).inc()
    REQUEST_LATENCY.labels(
        service=SERVICE_NAME,
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    # Логирование
    logger.info(
        json.dumps({
            "method": request.method,
            "endpoint": request.url.path,
            "status": status,
            "duration": duration
        })
    )
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/ping")
async def ping():
    return {"status": "ok"} 