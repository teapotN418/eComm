import logging
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time
import os
from datetime import datetime

SERVICE_NAME = os.getenv("SERVICE_NAME", "minio_service")

# Настройка логирования
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)

# Создаем JSON форматтер с нужными полями
json_formatter = jsonlogger.JsonFormatter(
    '%(time)s %(level)s %(service)s %(message)s'
)

# Настройка вывода в stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)

# Настройка вывода в файл
file_handler = logging.FileHandler('/var/log/minio_service/app.log')
file_handler.setFormatter(json_formatter)

logger.handlers = [console_handler, file_handler]

# Метрики Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status', 'service']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint', 'service']
)

def log_request(request: Request, response_time: float, status_code: int):
    """Логирование HTTP запроса"""
    log_data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "level": "INFO",
        "service": SERVICE_NAME,
        "message": f"{request.method} {request.url.path} {status_code} {response_time:.4f}s",
        "method": request.method,
        "url": str(request.url),
        "status_code": status_code,
        "response_time": response_time,
        "client_host": request.client.host if request.client else None
    }
    logger.info(log_data["message"], extra=log_data)
    
    # Обновляем метрики
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=status_code,
        service=SERVICE_NAME
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
        service=SERVICE_NAME
    ).observe(response_time)

def log_file_operation(operation: str, file_info: dict):
    """Логирование операций с файлами"""
    if 'filename' in file_info:
        file_info['file_name'] = file_info.pop('filename')
    log_data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "level": "INFO",
        "service": SERVICE_NAME,
        "message": f"{operation} {file_info}",
        "operation": operation,
        **file_info
    }
    logger.info(log_data["message"], extra=log_data) 