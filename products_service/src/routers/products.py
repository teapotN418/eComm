from fastapi import APIRouter, HTTPException

from src.repository.products import products_repo
from src.models.pydantic_schemas import ProductOut, ProductIn
from src.models.orm_models import Product

router = APIRouter()


@router.get('/', tags=['unauthorized'], response_model=list[ProductOut])
async def get_products(offset: int = 0, limit: int = 100):
    products = await products_repo.get_products(offset, limit)
    return products


@router.get('/{id}', tags=['unauthorized'], response_model=ProductOut)
async def get_product(id: int):
    product = await products_repo.get_product_by_id(id)
    if product == None:
        raise HTTPException(404, 'Product not found')
    return product


@router.post(
    '/',
    tags=['authorized'],
    response_model=ProductOut,
    status_code=201
)
async def insert_product(product: ProductIn):
    provider = await products_repo.get_provider_by_id(product.provider_id)
    if provider == None:
        raise HTTPException(409, 'The provider does not exist')

    category = await products_repo.get_category_by_id(product.category_id)
    if category == None:
        raise HTTPException(409, 'The category does not exist')

    new_product = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        minio_preview=product.minio_preview,
        provider_id=product.provider_id,
        category_id=product.category_id
    )

    new_product = await products_repo.insert_product(new_product)
    return new_product


@router.put(
    '/{id}',
    tags=['authorized'],
    response_model=ProductOut,
    status_code=201
)
async def update_product(id: int, new_data: ProductIn):
    product = await products_repo.get_product_by_id(id)
    if product == None:
        raise HTTPException(404, 'The product does not exist')

    provider = await products_repo.get_provider_by_id(new_data.provider_id)
    if provider == None:
        raise HTTPException(409, 'The provider does not exist')

    category = await products_repo.get_category_by_id(new_data.category_id)
    if category == None:
        raise HTTPException(409, 'The category does not exist')

    product.name = new_data.name
    product.price = new_data.price
    product.description = new_data.description
    product.minio_preview = new_data.minio_preview
    product.category_id = new_data.category_id
    product.provider_id = new_data.provider_id

    product = await products_repo.update_product(product)
    return product


@router.delete('/{id}', tags=['authorized'], status_code=204)
async def delete_product(id: int):
    product = await products_repo.get_product_by_id(id)
    if product == None:
        raise HTTPException(404, 'The product does not exist')

    await products_repo.delete_product_by_id(id)
