from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

from src.app.core.config import settings

security_config = AuthXConfig(
    JWT_ALGORITHM=settings.ALGORITHM,
    JWT_SECRET_KEY=settings.SECRET_KEY,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_CSRF_PROTECT = False,
)

security_obj = AuthX(config=security_config)