from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import status
from fastapi import Request, Response, HTTPException
import json
from datetime import datetime, timedelta, timezone

from src.app.api.schemas import Item, Cart
from src.app.core.config import settings

router = APIRouter()



async def get_cart_from_cookies(request: Request) -> Cart:
    cart_data = request.cookies.get(settings.CART_COOKIE_LOCATION)
    if cart_data:
        try:
            cart_dict = json.loads(cart_data)
            return Cart(**cart_dict)
        except (json.JSONDecodeError, ValueError):
            pass
    return Cart()

async def set_cart_to_cookies(response: Response, cart: Cart) -> None:
    cart_data = json.dumps(cart.model_dump())
    expires = datetime.now(timezone.utc) + timedelta(days=30)
    response.set_cookie(
        key=settings.CART_COOKIE_LOCATION,
        value=cart_data,
        expires=expires,
        httponly=True,
        secure=True,
        samesite='strict',
    )



@router.get("/cart", 
    response_model=Cart,
)
async def get_cart(
    request: Request,
):
    return await get_cart_from_cookies(request)



@router.post("/cart/items", 
    response_model=Cart,
)
async def add_item_to_cart(
    request: Request, 
    item: Item, 
    response: Response,
):
    cart = await get_cart_from_cookies(request)
    
    existing_item = next(
        (i for i in cart.items if i.product_id == item.product_id),
        None
    )
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        cart.items.append(item)
    
    await set_cart_to_cookies(response, cart)
    return cart



@router.put("/cart/items/{product_id}", 
    response_model=Cart,
)
async def update_cart_item(
    request: Request,
    product_id: int,
    quantity: int,
    response: Response,
):
    if quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be positive")
    
    cart = await get_cart_from_cookies(request)
    
    item = next(
        (i for i in cart.items if i.product_id == product_id),
        None
    )
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")
    
    item.quantity = quantity
    await set_cart_to_cookies(response, cart)
    return cart



@router.delete("/cart/items/{product_id}", 
    response_model=Cart,
)
async def remove_item_from_cart(
    request: Request,
    product_id: int,
    response: Response,
):
    cart = await get_cart_from_cookies(request)

    original_count = len(cart.items)
    
    cart.items = [item for item in cart.items if item.product_id != product_id]

    if len(cart.items) == original_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with product_id {product_id} not found in cart"
        )
    
    await set_cart_to_cookies(response, cart)
    return cart



@router.delete("/cart", 
    response_model=Cart,
)
async def clear_cart(
    request: Request, 
    response: Response,
):
    cart = await get_cart_from_cookies(request)
    cart.items = []
    await set_cart_to_cookies(response, cart)
    return cart