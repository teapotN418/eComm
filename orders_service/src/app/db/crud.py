from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.schemas.orders import OrderBase, OrderStatus
from src.app.db.models import OrdersORM

# async def get_user(user_id: int, session: AsyncSession):
#     query = select(OrdersORM).filter(OrdersORM.id==user_id)
#     result = await session.execute(query)
#     return result.scalars().first()

# async def get_user_by_email(email: str, session: AsyncSession):
#     query = select(OrdersORM).filter(OrdersORM.email==email)
#     result = await session.execute(query)
#     return result.scalars().first()

# async def get_users(skip: int, limit: int, session: AsyncSession):
#     query = select(OrdersORM).offset(skip).limit(limit)
#     result = await session.execute(query)
#     return result.scalars().all()

# async def create_user(user: UserCreate, session: AsyncSession):
#     hashed_password = await security.get_password_hash(user.password)
#     print(user)
#     db_user = OrdersORM(
#         email=user.email, hashed_password=hashed_password, role=user.role
#     )
#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)
#     return db_user

# async def delete_user(user: OrdersORM, session: AsyncSession):
#     query = delete(OrdersORM).where(OrdersORM.id == user.id)
#     await session.execute(query)
#     await session.commit()
#     return None
    
# async def update_user(user_id: int, new_password: str, session: AsyncSession):
#     user_instance = await session.get(OrdersORM, user_id)
#     user_instance.hashed_password = await security.get_password_hash(new_password)
#     await session.commit()
#     await session.refresh(user_instance)
#     return None

###################################################################################

async def get_order(cart_id: str, session: AsyncSession):
    query = select(OrdersORM).filter(OrdersORM.id == cart_id)
    result = await session.execute(query)
    return result.scalars().first()

async def create_order(order: OrderStatus, session: AsyncSession):
    order = OrdersORM(
        user_id=order.user_id, order_dict = order.order_dict, status = order.status,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order

# async def update_cart(
#     cart_id: str, 
#     update_data: dict, 
#     session: AsyncSession
# ) -> OrdersORM | None:
#     """Update cart data"""
#     query = (
#         update(OrdersORM)
#         .where(OrdersORM.id == cart_id)
#         .values(
#             cart_data=update_data,
#             updated_at=datetime.utcnow()
#         )
#         .returning(OrdersORM)
#     )
#     result = await session.execute(query)
#     await session.commit()
#     return result.scalars().first()

# async def update_cart_status(
#     cart_id: str, 
#     status: OrderStatus,
#     session: AsyncSession
# ) -> OrdersORM | None:
#     """Update cart status"""
#     query = (
#         update(OrdersORM)
#         .where(OrdersORM.id == cart_id)
#         .values(
#             status=status,
#             updated_at=datetime.utcnow()
#         )
#         .returning(OrdersORM)
#     )
#     result = await session.execute(query)
#     await session.commit()
#     return result.scalars().first()

# async def delete_cart(cart_id: str, session: AsyncSession) -> bool:
#     """Delete cart"""
#     query = delete(OrdersORM).where(OrdersORM.id == cart_id)
#     result = await session.execute(query)
#     await session.commit()
#     return result.rowcount > 0

# async def get_user_carts(
#     user_id: str, 
#     session: AsyncSession,
#     status: OrderStatus | None = None
# ) -> list[OrdersORM]:
#     """Get all carts for user with optional status filter"""
#     query = select(OrdersORM).filter(OrdersORM.user_id == user_id)
    
#     if status:
#         query = query.filter(OrdersORM.status == status)
        
#     result = await session.execute(query)
#     return result.scalars().all()

# async def get_active_cart_by_user(
#     user_id: str, 
#     session: AsyncSession
# ) -> OrdersORM | None:
#     """Get user's active cart"""
#     query = (
#         select(OrdersORM)
#         .filter(
#             OrdersORM.user_id == user_id,
#             OrdersORM.status == OrderStatus.ACTIVE
#         )
#         .order_by(OrdersORM.updated_at.desc())
#     )
#     result = await session.execute(query)
#     return result.scalars().first()