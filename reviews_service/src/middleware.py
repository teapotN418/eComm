import time
import logging
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('reviews_service')

# Метрики Prometheus
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['service', 'method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['service', 'method', 'endpoint']
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Получаем тело запроса
        body = None
        if request.method in ['POST', 'PUT']:
            try:
                body = await request.body()
                body = body.decode()
            except:
                body = "Could not decode body"
        
        # Выполняем запрос
        response = await call_next(request)
        
        # Вычисляем время выполнения
        process_time = time.time() - start_time
        
        # Логируем запрос
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time": f"{process_time:.3f}s",
            "body": body
        }
        logger.info(json.dumps(log_data))
        
        # Обновляем метрики
        http_requests_total.labels(
            service='reviews_service',
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            service='reviews_service',
            method=request.method,
            endpoint=request.url.path
        ).observe(process_time)
        
        return response 