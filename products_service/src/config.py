import os
import dotenv


class Config:

    dotenv.load_dotenv()

    POSTGRES_HOST = os.getenv('PRODUCTS_POSTGRES_HOST', 'localhost')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default')
    POSTGRES_PORT = os.getenv('PRODUCTS_POSTGRES_PORT', '5432')
    PRODUCTS_DB = os.getenv('PRODUCTS_POSTGRES_DB', 'db')
    POSTGRES_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{PRODUCTS_DB}'

    GATEWAY_URL = os.getenv('GATEWAY_URL', 'localhost')


config = Config()
