from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from src.config import config

Base = declarative_base()

engine = create_async_engine(
    url=config.POSTGRES_URL,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
