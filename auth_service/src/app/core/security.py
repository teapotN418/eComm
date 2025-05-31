from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

from src.app.core.config import settings

security_config = AuthXConfig(
    JWT_ALGORITHM=settings.ALGORITHM,
    JWT_SECRET_KEY=settings.SECRET_KEY,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_CSRF_PROTECT = False,
    JWT_ACCESS_TOKEN_EXPIRES = 300,
    JWT_REFRESH_TOKEN_EXPIRES = 86400,
)

security_obj = AuthX(config=security_config)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_tokens(id: int, data: dict):
    id = str(id)
    to_encode = data.copy()

    access_token = security_obj.create_access_token(id, data = to_encode, fresh=True)
    refresh_token = security_obj.create_refresh_token(id, data = to_encode)

    return (access_token, refresh_token)

async def refresh_access_token(id: int, data: dict):
    id = str(id)
    to_encode = data.copy()
    
    access_token = security_obj.create_access_token(id, data = to_encode, fresh=False)
    
    return access_token