from fastapi import APIRouter, Request
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response

from src.app.api.schemas import UserAuth, UserCreate, UserShow, Role, Password
from src.app.core import security
from src.app.db import crud
from src.app.api.deps import require_access, require_fresh_access, require_refresh, require_role, get_db, AsyncSession

router = APIRouter()

# @router.post("/startup",
#     summary="Remove table if exists and create again",
# )
# async def create_tables():
#     await crud.create_tables()
#     return {"detail": "Tokens set in cookies"}

@router.post("/admin",
    response_model=UserShow, 
)
async def make_admin(
    user: UserAuth,
    db: AsyncSession = Depends(get_db),
):
    db_user = await crud.get_user_by_email(email=user.email, session=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user_with_role = UserCreate(
        **user.model_dump(),
        role=Role.admin
    )
    result = await crud.create_user(user=user_with_role, session=db)
    return result

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

@router.post("/auth/login", 
    tags=["no-auth"],
)
async def login(
    response: Response,
    form_data: UserAuth,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(form_data.email, session=db)

    if not user or not await security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token, refresh_token = await security.create_tokens(user.email, {"role": user.role})
    
    response.set_cookie(key = security.security_config.JWT_ACCESS_COOKIE_NAME, 
                        value = access_token, path = security.security_config.JWT_ACCESS_COOKIE_PATH, samesite='strict')
    response.set_cookie(key = security.security_config.JWT_REFRESH_COOKIE_NAME, 
                        value = refresh_token, path = security.security_config.JWT_REFRESH_COOKIE_PATH, samesite='strict')
    return {"detail": "Tokens set in cookies"}

# ###################################################### auth

@router.post("/auth/refresh",
    tags=["authenticated"],
    dependencies=[Depends(require_refresh)],    
)
async def refresh_access_token(
    request: Request,
    response: Response,
):
    access_token = await security.refresh_access_token(request.state.sub, request.state.data)
    response.set_cookie(security.security_config.JWT_ACCESS_COOKIE_NAME, access_token, samesite='strict')
    return {"detail": "Access token refreshed"}



async def logout_func(response: Response):
    response.delete_cookie(security.security_config.JWT_ACCESS_COOKIE_NAME, security.security_config.JWT_ACCESS_COOKIE_PATH)
    response.delete_cookie(security.security_config.JWT_REFRESH_COOKIE_NAME, security.security_config.JWT_REFRESH_COOKIE_PATH)
    # ЖЕЛАТЕЛЬНО КОНЕЧНО ТОКЕНЫ ЕЩЁ ДОБАВЛЯТЬ В REVOKED

@router.post("/auth/logout", 
    tags=["authenticated"],
)
async def logout(
    response: Response,
):
    await logout_func(response)
    return {"detail": "Cookies removed"}



@router.get("/me", 
    tags=["authenticated"],
    response_model=UserCreate,
    dependencies=[Depends(require_access)],
)
async def read_profile(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(email=request.state.sub, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user



@router.put("/me",
    tags=["authenticated"],
    summary="Requires fresh access tokens",
    dependencies=[Depends(require_fresh_access)],
)
async def update_profile(
    request: Request, 
    password_form: Password,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(request.state.sub, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await crud.update_user(user.id, password_form.password, session=db)
    return {"detail": "Password changed"}



@router.delete("/me", 
    tags=["authenticated"],
    summary="Requires fresh access tokens",
    dependencies=[Depends(require_fresh_access)],
)
async def delete_profile(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(request.state.sub, session=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await crud.delete_user(user, session=db)
    await logout_func(response)
    return {"detail": "User deleted"}

# # ####################################################### admin

@router.get("",
    response_model=list[UserShow],
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
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
    dependencies=[Depends(require_role("admin"))],
    
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
    dependencies=[Depends(require_role("admin"))],
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
    dependencies=[Depends(require_role("admin"))],
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
    dependencies=[Depends(require_role("admin"))],
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