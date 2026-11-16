from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str
    jwt_algorithm: str
    jwt_secret: str
    access_token_expire_minutes: int
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket_name: str
    s3_endpoint_url: str
    s3_region: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
