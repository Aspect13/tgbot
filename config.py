import os
import logging
from pathlib import Path
from typing import Iterable

from aiogram import Bot, Dispatcher
from celery import Celery

from utils import Singleton, AppTG

logging.basicConfig(level=logging.INFO)


class Config(metaclass=Singleton):
    API_TOKEN = os.getenv('API_TOKEN')

    ROOT_DIR = Path(__file__).absolute().parent
    APPS_DIR = ROOT_DIR.joinpath('apps')

    broker_url = "amqp://aspect:aspect@localhost"
    redis_url = "redis://localhost"
    celery = Celery('tasks', broker=broker_url, backend=redis_url,)


    def __init__(self):
        assert self.API_TOKEN, 'API TOKEN IS REQUIRED'
        self.bot = Bot(token=self.API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.celery.conf.timezone = 'Europe/Moscow'

    def get_apps(self) -> Iterable[AppTG]:
        for i in self.APPS_DIR.iterdir():
            if i.is_dir() and i.joinpath('app.py').exists():
                yield AppTG(i)


config = Config()
