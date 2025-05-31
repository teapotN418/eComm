import os


class Config:

    POSTGRES_HOST = os.getenv('PRODUCTS_POSTGRES_HOST', 'localhost')
    POSTGRES_USER = os.getenv('PRODUCTS_POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD = os.getenv('PRODUCTS_POSTGRES_PASSWORD', 'default')
    POSTGRES_PORT = os.getenv('PRODUCTS_POSTGRES_PORT', '5432')
    PRODUCTS_DB = os.getenv('PRODUCTS_POSTGRES_DB', 'db')
    POSTGRES_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{PRODUCTS_DB}'

    GATEWAY_URL = os.getenv('GATEWAY_URL', 'localhost')

    ES_HOSTS = [os.getenv('ES_HOST', 'localhost')]
    ES_INDEX = os.getenv('ES_INDEX', 'products')


config = Config()
