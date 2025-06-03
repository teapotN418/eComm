from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status


from src.app.api.schemas import UserAuth, UserCreate, UserShow, Role, Password
from src.app.db import crud
from src.app.api.deps import get_db, AsyncSession, get_current_user, require_admin

router = APIRouter()


# no-auth

@router.post(
    "/register",
    response_model=UserShow,
    tags=["unauthorized"],
)
async def register(
    user: UserAuth,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user_by_email(email=user.email, session=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered")
    user_with_role = UserCreate(
        **user.model_dump(),
        role=Role.user
    )
    result = await crud.create_user(user=user_with_role, session=db)
    return result

# ###################################################### auth


@router.get(
    "",
    response_model=list[UserShow],
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    users = await crud.get_users(skip=skip, limit=limit, session=db)
    return users


@router.get("/profile/{user_id}", tags=["authorized"], response_model=UserShow)
async def read_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/profile/{user_id}", tags=["authorized"])
async def update_profile(
    user_id: int,
    password_form: Password,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await crud.update_user(user.id, password_form.password, session=db)
    return {"detail": "Password changed"}


@router.post(
    "",
    response_model=UserShow,
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user_by_email(email=user.email, session=db)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return await crud.create_user(user=user, session=db)


@router.get(
    "/by_id/{user_id}",
    response_model=UserShow,
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    "/by_id/{user_id}",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)
async def change_user(
    user_id: int,
    password_form: Password,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await crud.update_user(user_id, password_form.password, session=db)
    return {"detail": f"Password of user {user_id} changed"}


@router.delete(
    "/by_id/{user_id}",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await crud.delete_user(user=user, session=db)
    return {"detail": f"User with id {user_id} successfully deleted"}
