import logging
from operator import xor
from typing import Iterator

from pydantic import Field, RedisDsn, model_validator, field_validator, computed_field
from pydantic_core.core_schema import ValidationInfo

from utils import AppTG

logging.basicConfig(level=logging.INFO)

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

root_dir = Path(__file__).absolute().parent
app_dir = root_dir.joinpath('apps')


class RedisConfigMixin(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_password: Optional[str] = None

    redis_url: Optional[RedisDsn] = None

    @field_validator('redis_url', mode='after')
    @classmethod
    def make_redis_url(cls, v, info: ValidationInfo):
        if not v:
            host, port = info.data['redis_host'], info.data['redis_port']
            user, password = info.data['redis_user'], info.data['redis_password']
            auth = ''
            if user and password:
                auth = f'{user}:{password}@'
            return f'redis://{auth}{host}:{port}'
        return v

    @model_validator(mode='before')
    @classmethod
    def check_auth(cls, v):
        redis_user, redis_password = v.get('redis_user'), v.get('redis_password')
        assert not xor(redis_user is None, redis_password is None), 'provide redis auth at full, or not at all'
        return v


class Settings(RedisConfigMixin):
    model_config = SettingsConfigDict(
        env_file=root_dir.joinpath('.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )
    celery_redis_db: int = 0

    bot_token: str = Field(alias='tg_api_token')

    @computed_field(repr=True)
    @property
    def celery_broker_url(self) -> str:
        return f'{self.redis_url}/{self.celery_redis_db}'


settings = Settings()


def get_apps() -> Iterator[AppTG]:
    for i in app_dir.iterdir():
        if i.is_dir() and i.joinpath('app.py').exists():
            yield AppTG(i)

