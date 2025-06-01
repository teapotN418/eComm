from src.repository.db import async_session
from src.models.orm_models import Review
from sqlalchemy import select, func


class ReviewsRepo:

    async def get_review_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Review).where(Review.id == id)
            result = await session.execute(statement)
            return result.scalars().first()

    async def get_product_review_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Review).where(Review.product_id == id)

            result = await session.execute(statement)
            return result.scalars().all()

    async def get_user_review_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Review).where(Review.user_id == id)

            result = await session.execute(statement)
            return result.scalars().all()

    async def get_avg_score_by_product_id(self, id: int):
        async with async_session() as session:
            statement = select(
                func.round(func.avg(Review.score), 2).label('score')
            ).where(Review.product_id == id)

            result = await session.execute(statement)
            return result.scalars().first()

    async def insert_review(self, review: Review):
        async with async_session() as session:
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review

    async def update_review(self, review: Review):
        async with async_session() as session:
            merged_review = await session.merge(review)
            await session.commit()
            await session.refresh(merged_review)
            return merged_review

    async def delete_review_by_id(self, id: int):
        async with async_session() as session:
            statement = select(Review).where(Review.id == id)
            review = (await session.execute(statement)).scalars().first()

            await session.delete(review)
            await session.commit()
            return True


reviews_repo = ReviewsRepo()
