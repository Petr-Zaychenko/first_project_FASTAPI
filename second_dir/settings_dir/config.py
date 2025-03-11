from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import Field
from celery import Celery

load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    BROKER_USER: str = Field(default="guest")
    BROKER_PASS: str = Field(default="guest")
    BROKER_PORT: int = Field(default=5672)

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def CELERY_BROKER_URL(self):
        return f"pyamqp://{self.BROKER_USER}:{self.BROKER_PASS}@rabbitmq:{self.BROKER_PORT}//"


    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend="rpc://"
)