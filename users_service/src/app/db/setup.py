from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)

async_session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

class Base(DeclarativeBase):
    pass