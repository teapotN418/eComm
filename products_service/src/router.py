from fastapi import APIRouter

router = APIRouter()


@router.get('/', tags=['authorized'])
async def hello():
    return 'Hello, world!'
