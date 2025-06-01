from src.repository.db import async_session
from src.models.orm_models import Provider, Category, Product
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class ProductsRepo:

    # Providers

    async def get_providers(self, offset: int, limit: int):
        async with async_session() as session:
            statement = select(Provider).order_by(
                Provider.id
            ).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_provider_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Provider).where(Provider.id == id)
            result = await session.execute(statement)
            return result.scalars().first()

    async def insert_provider(self, provider: Provider):
        async with async_session() as session:
            session.add(provider)
            await session.commit()
            await session.refresh(provider)
            return provider

    async def update_provider(self, provider: Provider):
        async with async_session() as session:
            merged_provider = await session.merge(provider)
            await session.commit()
            await session.refresh(merged_provider)
            return merged_provider

    async def delete_provider_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Provider).where(Provider.id == id)
            provider = (await session.execute(statement)).scalars().first()

            await session.delete(provider)
            await session.commit()
            return True

    # Products

    async def get_products(self, offset: int, limit: int):
        async with async_session() as session:
            statement = select(Product).options(
                joinedload(Product.provider),
                joinedload(Product.category)
            ).order_by(
                Product.id
            ).offset(offset).limit(limit)

            result = await session.execute(statement)
            return result.scalars().all()

    async def get_product_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Product).options(
                joinedload(Product.provider),
                joinedload(Product.category)
            ).where(Product.id == id)

            result = await session.execute(statement)
            return result.scalars().first()

    async def get_found_products(self, ids: list[int]):
        async with async_session() as session:
            statement = select(Product).options(
                joinedload(Product.provider),
                joinedload(Product.category)
            ).where(Product.id.in_(ids))

            result = await session.execute(statement)
            return result.scalars().all()

    async def insert_product(self, product: Product):
        async with async_session() as session:
            session.add(product)
            await session.commit()
            await session.refresh(product)
            product = await self.get_product_by_id(product.id)
            return product

    async def update_product(self, product: Product):
        async with async_session() as session:
            merged_product = await session.merge(product)
            await session.commit()
            await session.refresh(merged_product)
            return merged_product

    async def delete_product_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Product).where(Product.id == id)
            product = (await session.execute(statement)).scalars().first()

            await session.delete(product)
            await session.commit()
            return True

    # Categories

    async def get_categories(self, offset: int, limit: int):
        async with async_session() as session:
            statement = select(Category).order_by(
                Category.id
            ).offset(offset).limit(limit)
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_category_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Category).where(Category.id == id)
            result = await session.execute(statement)
            return result.scalars().first()

    async def insert_category(self, category: Category):
        async with async_session() as session:
            session.add(category)
            await session.commit()
            await session.refresh(category)
            return category

    async def update_category(self, category: Category):
        async with async_session() as session:
            merged_category = await session.merge(category)
            await session.commit()
            await session.refresh(merged_category)
            return merged_category

    async def delete_category_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Category).where(Category.id == id)
            category = (await session.execute(statement)).scalars().first()

            await session.delete(category)
            await session.commit()
            return True


products_repo = ProductsRepo()
