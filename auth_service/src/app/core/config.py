from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import tomllib
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent.parent
with open(f"{PROJECT_DIR}/pyproject.toml", "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["project"]


class Settings(BaseSettings):
    ALGORITHM: str
    SECRET_KEY: str

    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    POSTGRES_HOST: str = Field(alias="USERS_POSTGRES_HOST")
    POSTGRES_PORT: str = Field(alias="USERS_POSTGRES_PORT")
    POSTGRES_DB: str = Field(alias="USERS_POSTGRES_DB")
    POSTGRES_USER: str = Field(alias="USERS_POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(alias="USERS_POSTGRES_PASSWORD")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
