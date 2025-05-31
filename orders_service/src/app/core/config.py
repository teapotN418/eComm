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

    BACKEND_PORT: str = Field(alias="ORDERS_PORT")
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()