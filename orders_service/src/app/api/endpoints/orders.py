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

# def require_admin(
#     x_user_id: str = Header(...),
#     x_user_role: str = Header(...),
# ):
#     if x_user_role != "admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
#     return {"id": int(x_user_id), "role": x_user_role}

# def get_current_user(
#     x_user_id: str = Header(...),
#     x_user_role: str = Header(...),
# ):
#     return {"id": int(x_user_id), "role": x_user_role}

from fastapi import Header, HTTPException, status, Depends

async def get_current_user_id(x_user_id: str = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return int(x_user_id)

async def require_authenticated_user(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: user_id mismatch")

async def require_admin(x_user_role: str = Header(None)):
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")

########################### authenticated

@router.post("/{user_id}", 
    tags=["authenticated"],
    response_model=OrderOut,
    dependencies=[Depends(require_authenticated_user)]
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
    dependencies=[Depends(require_authenticated_user)]
)
async def get_orders_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    orders = await crud.get_orders_by_user(user_id, db)
    return orders

# ########################### admin

@router.get("/{user_id}", 
    tags=["admin"],
    response_model=list[OrderOut],
)
async def get_orders_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    orders = await crud.get_orders_by_user(user_id, db)
    return orders

@router.get("",
    response_model=list[OrderOut],
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def get_all_orders(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    orders = await crud.get_orders(skip=skip, limit=limit, session=db)
    return orders

@router.get("/{order_id}", 
    tags=["admin"],
    response_model=OrderOut,
    dependencies=[Depends(require_admin)]
)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
):
    order = await crud.get_order_by_id(order_id, db)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No order {order_id} found"
        )
    return order

@router.put("/{order_id}", 
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def change_order(
    order_id: int,
    order_status: Status,
    db: AsyncSession = Depends(get_db),
):
    order = await crud.get_order_by_id(order_id, db)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No order {order_id} found"
        )
    changed_order = await crud.change_status(order_id, order_status, db)
    return changed_order

@router.delete("/{order_id}", 
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def remove_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
):
    order = await crud.get_order_by_id(order_id, db)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No order {order_id} found"
        )
    await crud.delete_order(order_id, db)
    return {"detail": f"Order with id {order_id} successfully deleted"}