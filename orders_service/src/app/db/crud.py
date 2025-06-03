from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.api.schemas.orders import OrderStatus
from src.app.db.models import OrdersORM, ItemsORM

async def get_order_by_id(order_id: int, session: AsyncSession):
    query = select(OrdersORM).filter(OrdersORM.id == order_id).options(selectinload(OrdersORM.items))
    result = await session.execute(query)
    return result.scalars().first()

async def get_orders_by_user(user_id: int, session: AsyncSession):
    query = select(OrdersORM).filter(OrdersORM.user_id == user_id).options(selectinload(OrdersORM.items))
    result = await session.execute(query)
    return result.scalars().all()

async def create_order(order: OrderStatus, order_data, session: AsyncSession):
    order_obj = OrdersORM(
        user_id=order.user_id, status = order.status,
    )
    for (id, q) in order_data:
        item_obj = ItemsORM(product_id=id, quantity = q)
        order_obj.items.append(item_obj)
    session.add(order_obj)
    await session.commit()
    await session.refresh(order_obj)
    order_created = await get_order_by_id(order_obj.id, session)
    return order_created

async def get_orders(skip: int, limit: int, session: AsyncSession):
    query = select(OrdersORM).offset(skip).limit(limit).options(selectinload(OrdersORM.items))
    result = await session.execute(query)
    return result.scalars().all()

async def change_status(order_id: int, status: str, session: AsyncSession):
    order_instance = await session.get(OrdersORM, order_id)
    order_instance.status = status
    await session.commit()
    await session.refresh(order_instance)
    order_changed = await get_order_by_id(order_instance.id, session)
    return order_changed

async def delete_order(order_id: int, session: AsyncSession):
    query = delete(OrdersORM).where(OrdersORM.id == order_id)
    await session.execute(query)
    await session.commit()
    return None