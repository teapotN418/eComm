import os


class Config:
    POSTGRES_HOST = os.getenv('REVIEWS_POSTGRES_HOST', 'localhost')
    POSTGRES_USER = os.getenv('REVIEWS_POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD = os.getenv('REVIEWS_POSTGRES_PASSWORD', 'default')
    POSTGRES_PORT = os.getenv('REVIEWS_POSTGRES_PORT', '5432')
    PRODUCTS_DB = os.getenv('REVIEWS_POSTGRES_DB', 'db')
    POSTGRES_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{PRODUCTS_DB}'

    GATEWAY_URL = os.getenv('GATEWAY_URL', 'localhost')


config = Config()
