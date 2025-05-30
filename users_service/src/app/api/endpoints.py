from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response

from src.app.api.schemas import UserAuth, UserCreate, UserShow, Role, Password
from src.app.core import security
from src.app.db import crud
from src.app.api.deps import get_db, AsyncSession

router = APIRouter()


###################################################### no-auth

@router.post("/register", 
    response_model=UserShow, 
    tags=["no-auth"],
)
async def register(
    user: UserAuth,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user_by_email(email=user.email, session=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user_with_role = UserCreate(
        **user.model_dump(),
        role=Role.user
    )
    result = await crud.create_user(user=user_with_role, session=db)
    return result

# ###################################################### auth

@router.get("/profile/{user_id}", 
    tags=["authenticated"],
    response_model=UserShow,
)
async def read_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user



@router.put("/profile/{user_id}", 
    tags=["authenticated"],
)
async def update_profile(
    user_id: int,
    password_form: Password,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await crud.update_user(user.id, password_form.password, session=db)
    return {"detail": "Password changed"}



@router.delete("/profile/{user_id}", 
    tags=["authenticated"],
)
async def delete_profile(
    user_id: int,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user(user_id=user_id, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await crud.delete_user(user, session=db)
    response.delete_cookie(security.security_config.JWT_ACCESS_COOKIE_NAME, security.security_config.JWT_ACCESS_COOKIE_PATH)
    response.delete_cookie(security.security_config.JWT_REFRESH_COOKIE_NAME, security.security_config.JWT_REFRESH_COOKIE_PATH)
    # ЖЕЛАТЕЛЬНО КОНЕЧНО ТОКЕНЫ ЕЩЁ ДОБАВЛЯТЬ В REVOKED
    return {"detail": "User deleted"}

# # ####################################################### admin

@router.get("",
    response_model=list[UserShow],
    tags=["admin"],
)
async def read_users(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    users = await crud.get_users(skip=skip, limit=limit, session=db)
    return users



@router.post("", 
    response_model=UserShow, 
    tags=["admin"],
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user_by_email(email=user.email, session=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    result = await crud.create_user(user=user, session=db)
    return result



@router.get("/{user_id}", 
    response_model=UserShow, 
    tags=["admin"],
)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user(user_id=user_id, session=db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user



@router.put("/{user_id}", 
    tags=["admin"],
)
async def change_user(
    user_id: int, 
    password_form: Password,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user(user_id=user_id, session=db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await crud.update_user(user_id, password_form.password, session=db)
    return {"detail": f"Password of user {user_id} changed"}



@router.delete("/{user_id}", 
    tags=["admin"],
)
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user(user_id=user_id, session=db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await crud.delete_user(user=db_user, session=db)
    return {"detail": f"User with id {user_id} successfully deleted"}