from fastapi import APIRouter, HTTPException
from elasticsearch import AsyncElasticsearch
from fastapi import Header
from fastapi import Depends, status

from src.repository.products import products_repo
from src.models.pydantic_schemas import ProductOut, ProductIn
from src.models.orm_models import Product
from src.config import config

router = APIRouter()
es_client = AsyncElasticsearch(hosts=config.ES_HOSTS)


def require_admin(
    x_user_id: str = Header(...),
    x_user_role: str = Header(...),
):
    if x_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return {"id": int(x_user_id), "role": x_user_role}


@router.get('/', tags=['unauthorized'], response_model=list[ProductOut])
async def get_products(offset: int = 0, limit: int = 100):
    products = await products_repo.get_products(offset, limit)
    return products


@router.get('/search', tags=['unauthorized'], response_model=list[ProductOut])
async def get_products(string: str):
    es_query = {
        "size": 20,
        "query": {
            "bool": {
                "should": [
                    {
                        "match_phrase": {  # Точное совпадение названия продукта
                            "name": {
                                "query": string,
                                "boost": 200  # Максимальный приоритет точному совпадению
                            }
                        }
                    },
                    {
                        "multi_match": {  # Частичное совпадение в названии
                            "query": string,
                            "fields": ["name^5"],
                            "boost": 20
                        }
                    },
                    {
                        "multi_match": {  # Поиск по описанию
                            "query": string,
                            "fields": ["description^1"],
                            "boost": 5
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        },
        "sort": [
            {
                "_score": {  # Сортировка только по релевантности
                    "order": "desc"
                }
            }
        ]
    }

    result = await es_client.search(index=config.ES_INDEX, body=es_query)
    ids = [hit["_source"]["id"] for hit in result["hits"]["hits"]]

    products = await products_repo.get_found_products(ids)
    return products


@router.get('/{id}', tags=['unauthorized'], response_model=ProductOut)
async def get_product(id: int):
    product = await products_repo.get_product_by_id(id)
    if product == None:
        raise HTTPException(404, 'Product not found')
    return product


@router.post(
    '/',
    tags=['admin'], dependencies=[Depends(require_admin)],
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
    tags=['admin'], dependencies=[Depends(require_admin)],
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


@router.delete('/{id}', tags=['admin'], dependencies=[Depends(require_admin)], status_code=204)
async def delete_product(id: int):
    product = await products_repo.get_product_by_id(id)
    if product == None:
        raise HTTPException(404, 'The product does not exist')

    await products_repo.delete_product_by_id(id)
