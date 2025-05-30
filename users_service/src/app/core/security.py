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

async def get_password_hash(password):
    return pwd_context.hash(password)