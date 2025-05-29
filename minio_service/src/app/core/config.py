from pydantic_settings import BaseSettings, SettingsConfigDict
import tomllib
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent.parent
with open(f"{PROJECT_DIR}/pyproject.toml", "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["project"]

class Settings(BaseSettings):

    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    ALGORITHM: str
    SECRET_KEY: str

    MINIO_PORT: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()