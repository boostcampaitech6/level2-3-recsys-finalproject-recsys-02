from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    storage_path: str = Field(default="./storage", env="MODEL_PATH")
    # app_env: str = Field(default="local", env="APP_ENV")
    account_json_path: str = Field(default="../storage/level3-416207-893f91c9529e", env="SERVICE_ACCOUNT_FILE")
    project_id: str = Field(default="level3-416207", env="PROJECT_ID")
    bucket_name: str = Field(default="crwalnoti", env="BUCKET_NAME")

    # download_model
    artifact_uri: str = Field(default="runs:/9c5dfe82b5e744a7bc2087e63113c9c6/model", env="ARTIFACT_URI")
    run_id: str = Field(default="9c5dfe82b5e744a7bc2087e63113c9c6")
config = Config()