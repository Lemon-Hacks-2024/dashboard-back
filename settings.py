import logging.config
import os

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET: str
    EXPIRE_TIME: int
    ALGORITHM: str
    S3_CLOUD_KEY: str
    S3_CLOUD_SECRET: str
    BUCKET_NAME: str
    BUCKET_PUBLIC_PATH: str
    MODE: int
    ACCESS_TOKEN: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def mode(self):
        if self.MODE == 0:
            return True
        else:
            return False

    model_config = SettingsConfigDict(env_file=os.path.abspath(".env"))


with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


settings = Settings()


