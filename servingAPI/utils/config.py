from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    storage_path: str = Field(default="./storage", env="MODEL_PATH")
    # app_env: str = Field(default="local", env="APP_ENV")
    account_json_path: str = Field(default="storage/level3-416207-893f91c9529e.json", env="SERVICE_ACCOUNT_FILE")
    project_id: str = Field(default="level3-416207", env="PROJECT_ID")
    bucket_name: str = Field(default="crwalnoti", env="BUCKET_NAME")

    # model_path
    download_model_path: str = Field(default="storage/model/SASRec.pt", env="MODEL_PATH")
config = Config()