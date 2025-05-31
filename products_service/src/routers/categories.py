from fastapi import APIRouter, HTTPException

from src.repository.products import products_repo
from src.models.pydantic_schemas import CategoryOut, CategoryIn
from src.models.orm_models import Category

router = APIRouter()


@router.get('/', tags=['unauthorized'], response_model=list[CategoryOut])
async def get_categories(offset: int = 0, limit: int = 100):
    categories = await products_repo.get_categories(offset, limit)
    return categories


@router.get('/{id}', tags=['unauthorized'], response_model=CategoryOut)
async def get_category(id: int):
    category = await products_repo.get_category_by_id(id)
    if category == None:
        raise HTTPException(404, 'Category not found')
    return category


@router.post(
    '/',
    tags=['authorized'],
    response_model=CategoryOut,
    status_code=201
)
async def create_category(category: CategoryIn):
    new_cat = Category(name=category.name)
    new_cat = await products_repo.insert_category(new_cat)
    return new_cat


@router.put(
    '/{id}',
    tags=['authorized'],
    response_model=CategoryOut,
    status_code=201
)
async def update_category(id: int, new_data: CategoryIn):
    category = await products_repo.get_category_by_id(id)
    if category == None:
        raise HTTPException(404, 'The category has not yet been created')
    category.name = new_data.name
    category = await products_repo.update_category(category)
    return category


@router.delete('/{id}', tags=['authorized'], status_code=204)
async def update_category(id: int):
    category = await products_repo.get_category_by_id(id)
    if category == None:
        raise HTTPException(404, 'The category does not exist')
    await products_repo.delete_category_by_id(id)
