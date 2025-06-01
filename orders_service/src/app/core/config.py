from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import tomllib
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent.parent
with open(f"{PROJECT_DIR}/pyproject.toml", "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["project"]

class Settings(BaseSettings):

    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    CART_COOKIE_LOCATION: str

    POSTGRES_HOST: str = Field(alias="ORDERS_POSTGRES_HOST")
    POSTGRES_PORT: str = Field(alias="ORDERS_POSTGRES_PORT")
    POSTGRES_DB: str = Field(alias="ORDERS_POSTGRES_DB")
    POSTGRES_USER: str = Field(alias="ORDERS_POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(alias="ORDERS_POSTGRES_PASSWORD")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    BACKEND_PORT: str = Field(alias="ORDERS_PORT")
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()