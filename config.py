import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    def __init__(self, **data):
        super().__init__(**data)
        for field_name, field_value in self.model_dump().items():
            if field_value is not None:
                os.environ[field_name] = str(field_value)
