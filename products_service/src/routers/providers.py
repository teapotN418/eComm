from fastapi import APIRouter, HTTPException

from src.repository.products import products_repo
from src.models.pydantic_schemas import ProviderOut, ProviderIn
from src.models.orm_models import Provider

router = APIRouter()


@router.get('/', tags=['unauthorized'], response_model=list[ProviderOut])
async def get_providers(offset: int = 0, limit: int = 100):
    providers = await products_repo.get_providers(offset, limit)
    return providers


@router.get('/{id}', tags=['unauthorized'], response_model=ProviderOut)
async def get_provider(id: int):
    provider = await products_repo.get_provider_by_id(id)
    if provider == None:
        raise HTTPException(404, 'Provider not found')
    return provider


@router.post(
    '/',
    tags=['authorized'],
    response_model=ProviderOut,
    status_code=201
)
async def insert_provider(provider: ProviderIn):
    new_provider = Provider(
        name=provider.name,
        email=provider.email,
        address=provider.address
    )
    new_provider = await products_repo.insert_provider(new_provider)
    return new_provider


@router.put(
    '/{id}',
    tags=['authorized'],
    response_model=ProviderOut,
    status_code=201
)
async def update_provider(id: int, new_data: ProviderIn):
    provider = await products_repo.get_provider_by_id(id)
    if provider == None:
        raise HTTPException(404, 'The provider does not exist')

    provider.name = new_data.name
    provider.email = new_data.email
    provider.address = new_data.address

    provider = await products_repo.update_provider(provider)
    return provider


@router.delete('/{id}', tags=['authorized'], status_code=204)
async def delete_provider(id: int):
    provider = await products_repo.get_provider_by_id(id)
    if provider == None:
        raise HTTPException(404, 'The provider does not exist')

    await products_repo.delete_provider_by_id(id)
