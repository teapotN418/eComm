from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.config import config
from src.router import router

openapi_tags = [
    {'name': 'unauthorized', 'description': 'Does not require authorization'},
    {'name': 'authorized', 'description': 'Requires proper authorization'}
]

app = FastAPI(
    openapi_tags=openapi_tags,
    docs_url='/docs'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.GATEWAY_URL],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['*']
)

app.include_router(router, prefix='/api/reviews')
