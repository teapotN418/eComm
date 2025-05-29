from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models import UsersORM

async def get_user_by_email(email: str, session: AsyncSession):
    query = select(UsersORM).filter(UsersORM.email==email)
    result = await session.execute(query)
    return result.scalars().first()