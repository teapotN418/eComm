from fastapi import APIRouter

from src.repository.products import products_repo
from src.models.pydantic_schemas import CategoryOut, ProviderOut, ProductOut

router = APIRouter()


@router.get('/', tags=['unauthorized'], response_model=list[ProductOut])
async def get_products(
    offset: int = 0,
    limit: int = 100
):
    products = await products_repo.get_products(offset, limit)
    return products
