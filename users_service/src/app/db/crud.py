from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.schemas import UserCreate
from src.app.core import security
from src.app.db.models import UsersORM
from src.app.db.setup import async_session_factory


# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

async def get_user(user_id: int, session: AsyncSession):
    #async with async_session_factory() as session:
    query = select(UsersORM).filter(UsersORM.id==user_id)
    result = await session.execute(query)
    return result.scalars().first()

async def get_user_by_email(email: str, session: AsyncSession):
    #async with async_session_factory() as session:
    query = select(UsersORM).filter(UsersORM.email==email)
    result = await session.execute(query)
    return result.scalars().first()

async def get_users(skip: int, limit: int, session: AsyncSession):
    #async with async_session_factory() as session:
    query = select(UsersORM).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

async def create_user(user: UserCreate, session: AsyncSession):
    #async with async_session_factory() as session:
    hashed_password = await security.get_password_hash(user.password)
    print(user)
    db_user = UsersORM(
        email=user.email, hashed_password=hashed_password, role=user.role
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def delete_user(user: UsersORM, session: AsyncSession):
    #async with async_session_factory() as session:
    query = delete(UsersORM).where(UsersORM.id == user.id)
    await session.execute(query)
    await session.commit()
    return None
    
async def update_user(user_id: int, new_password: str, session: AsyncSession):
    #async with async_session_factory() as session:
    user_instance = await session.get(UsersORM, user_id)
    user_instance.hashed_password = await security.get_password_hash(new_password)
    await session.commit()
    await session.refresh(user_instance)
    return None
