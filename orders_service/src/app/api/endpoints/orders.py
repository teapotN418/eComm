from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import status
from fastapi import Request, Response, HTTPException
from fastapi import Depends

import src.app.db.crud as crud
from src.app.api.schemas.orders import OrderStatus, Status, OrderOut
from src.app.api.deps import get_db, AsyncSession
from .cart import get_cart_from_cookies

router = APIRouter()

########################### authenticated

@router.post("/{user_id}", 
    tags=["authenticated"],
    response_model=OrderOut,
)
async def create_order(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    cart = await get_cart_from_cookies(request)
    try:
        if len(cart.pr)==0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )
        order_data = [(item["id"], item["q"]) for item in cart.model_dump()["pr"]]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}"
        )
    order_with_status = OrderStatus(
        user_id = user_id,
        status=Status.created,
    )
    order = await crud.create_order(order_with_status, order_data, db)
    return order

@router.get("/me/{user_id}", 
    tags=["authenticated"],
    response_model=list[OrderOut],
)
async def get_orders_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    orders = await crud.get_orders_by_user(user_id, db)
    return orders

# ########################### admin

@router.get("",
    response_model=list[OrderOut],
    tags=["admin"],
)
async def get_all_orders(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    orders = await crud.get_orders(skip=skip, limit=limit, session=db)
    return orders

@router.get("/{order_id}", 
    tags=["authenticated"],
    response_model=OrderOut,
)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
):
    order = await crud.get_order_by_id(order_id, db)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No order found"
        )
    return order

# @router.put("/{order_id}", 
#     tags=["authenticated"],
# )
# async def create_order(
#     request: Request,
#     user_id: int,
#     db: AsyncSession = Depends(get_db),
# ):
#     cart = await get_cart_from_cookies(request)
#     if len(cart.pr)==0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
#         )
#     order_with_status = OrderStatus(
#         user_id = user_id,
#         status=Status.created,
#     )
#     try:
#         order_data = [(item["id"], item["q"]) for item in cart.model_dump()["pr"]]
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}"
#         )
#     order = await crud.create_order(order_with_status, order_data, db)
#     return order

# @router.delete("/{order_id}", 
#     tags=["authenticated"],
# )
# async def create_order(
#     request: Request,
#     user_id: int,
#     db: AsyncSession = Depends(get_db),
# ):
#     cart = await get_cart_from_cookies(request)
#     if len(cart.pr)==0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
#         )
#     order_with_status = OrderStatus(
#         user_id = user_id,
#         status=Status.created,
#     )
#     try:
#         order_data = [(item["id"], item["q"]) for item in cart.model_dump()["pr"]]
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}"
#         )
#     order = await crud.create_order(order_with_status, order_data, db)
#     return order