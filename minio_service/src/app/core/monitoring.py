import logging
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time

SERVICE_NAME = "minio_service"

# Настройка логирования
logger = logging.getLogger("minio_service")
logger.setLevel(logging.INFO)

# Создаем JSON форматтер
json_formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)
logger.handlers = [console_handler]

# Метрики Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['service', 'method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['service', 'method', 'endpoint']
)

def log_request(request: Request, response_time: float, status_code: int):
    """Логирование HTTP запроса"""
    log_data = {
        "method": request.method,
        "url": str(request.url),
        "status_code": status_code,
        "response_time": response_time,
        "client_host": request.client.host if request.client else None
    }
    logger.info("HTTP Request", extra=log_data)
    
    # Обновляем метрики
    REQUEST_COUNT.labels(
        service=SERVICE_NAME,
        method=request.method,
        endpoint=request.url.path,
        status=status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        service=SERVICE_NAME,
        method=request.method,
        endpoint=request.url.path
    ).observe(response_time)

def log_file_operation(operation: str, file_info: dict):
    """Логирование операций с файлами"""
    if 'filename' in file_info:
        file_info['file_name'] = file_info.pop('filename')
    log_data = {
        "operation": operation,
        **file_info
    }
    logger.info("File Operation", extra=log_data) 