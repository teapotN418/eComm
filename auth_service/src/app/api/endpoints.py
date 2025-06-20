from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response

from src.app.api.schemas import UserAuth, Role, ID
from src.app.core import security
from src.app.db import crud
from src.app.api.deps import require_access, require_refresh, get_db, AsyncSession


router = APIRouter()


@router.post("/login", tags=['unauthorized'])
async def login(
    form_data: UserAuth,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_email(form_data.email, session=db)

    if not user or not await security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token, refresh_token = await security.create_tokens(user.id, {"role": user.role})

    response.set_cookie(key=security.security_config.JWT_ACCESS_COOKIE_NAME,
                        value=access_token, path=security.security_config.JWT_ACCESS_COOKIE_PATH, samesite='lax')
    response.set_cookie(key=security.security_config.JWT_REFRESH_COOKIE_NAME,
                        value=refresh_token, path=security.security_config.JWT_REFRESH_COOKIE_PATH, samesite='lax')
    return {"detail": "Tokens set in cookies"}


@router.get("/verify", tags=["authorized"], dependencies=[Depends(require_access)])
async def verify_token(request: Request):
    return Response(
        status_code=200,
        headers={
            "X-User-ID": str(request.state.sub),
            "X-User-Role": request.state.data.get("role", "")
        }
    )


# @router.post(
#     "/verify-role",
#     tags=["authorized"],
#     response_model=ID,
#     dependencies=[Depends(require_access)],
# )
# async def verify_token_role(
#     role: Role,
#     request: Request,
# ):
#     if request.state.data.get("role") == role:
#         return ID(id=request.state.sub)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#         )


@router.post(
    "/refresh",
    tags=["authorized"],
    dependencies=[Depends(require_refresh)],
)
async def refresh_access_token(
    request: Request,
    response: Response,
):
    access_token = await security.refresh_access_token(request.state.sub, request.state.data)
    response.set_cookie(
        security.security_config.JWT_ACCESS_COOKIE_NAME, access_token, samesite='strict')
    return {"detail": "Access token refreshed"}


@router.post(
    "/logout",
    tags=["authorized"],
)
async def logout(
    response: Response,
):
    response.delete_cookie(security.security_config.JWT_ACCESS_COOKIE_NAME,
                           security.security_config.JWT_ACCESS_COOKIE_PATH)
    response.delete_cookie(security.security_config.JWT_REFRESH_COOKIE_NAME,
                           security.security_config.JWT_REFRESH_COOKIE_PATH)

    return {"detail": "Cookies removed"}
