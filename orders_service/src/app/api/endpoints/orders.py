from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import status
from fastapi import Request, Response, HTTPException
from fastapi import Depends

import src.app.db.crud as crud
from src.app.api.schemas.orders import OrderBase, OrderStatus, Status
from src.app.core.config import settings
from src.app.api.deps import get_db, AsyncSession
from .cart import get_cart_from_cookies, Cart

router = APIRouter()

@router.post("/{user_id}", 
    tags=["authenticated"],
    response_model=OrderStatus,
)
async def create_order(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    cart = await get_cart_from_cookies(request)
    if len(cart.pr)==0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )
    order_with_status = OrderStatus(
        user_id = user_id,
        order_dict=cart.model_dump(),
        status=Status.created,
    )
    order = await crud.create_order(order_with_status, db)
    return order
    

# @router.get("/profile/{user_id}", 
#     tags=["authenticated"],
#     response_model=UserShow,
# )
# async def read_profile(
#     user_id: int,
#     db: AsyncSession = Depends(get_db),
# ):
#     user = await crud.get_user(user_id=user_id, session=db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     return user



# @router.put("/profile/{user_id}", 
#     tags=["authenticated"],
# )
# async def update_profile(
#     user_id: int,
#     password_form: Password,
#     db: AsyncSession = Depends(get_db),
# ):
#     user = await crud.get_user(user_id=user_id, session=db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     await crud.update_user(user.id, password_form.password, session=db)
#     return {"detail": "Password changed"}



# @router.delete("/profile/{user_id}", 
#     tags=["authenticated"],
# )
# async def delete_profile(
#     user_id: int,
#     # response: Response,
#     db: AsyncSession = Depends(get_db),
# ):
#     user = await crud.get_user(user_id=user_id, session=db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     await crud.delete_user(user, session=db)
#     # response.delete_cookie(security.security_config.JWT_ACCESS_COOKIE_NAME, security.security_config.JWT_ACCESS_COOKIE_PATH)
#     # response.delete_cookie(security.security_config.JWT_REFRESH_COOKIE_NAME, security.security_config.JWT_REFRESH_COOKIE_PATH)
#     # ЖЕЛАТЕЛЬНО КОНЕЧНО ТОКЕНЫ ЕЩЁ ДОБАВЛЯТЬ В REVOKED
#     return {"detail": "User deleted"}