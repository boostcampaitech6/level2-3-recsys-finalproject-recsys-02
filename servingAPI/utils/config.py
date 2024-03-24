from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    storage_path: str = Field(default="./storage", env="MODEL_PATH")
    # app_env: str = Field(default="local", env="APP_ENV")
    

config = Config()