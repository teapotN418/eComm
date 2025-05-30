from src.repository.db import async_session
from src.models.orm_models import Provider, Category, Product
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class ProductsRepo:
    async def get_providers(self, offset, limit):
        async with async_session() as session:
            statement = select(Provider).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_products(self, offset, limit):
        async with async_session() as session:
            statement = select(Product).options(joinedload(Product.provider), joinedload(
                Product.category)).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.scalars().all()


products_repo = ProductsRepo()
