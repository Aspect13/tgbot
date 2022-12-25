import os
import logging
from pathlib import Path
from typing import Iterable

from aiogram import Bot, Dispatcher
from celery import Celery

from utils import Singleton, AppTG

logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv

load_dotenv()


class Config(metaclass=Singleton):
    TG_API_TOKEN = os.getenv('TG_API_TOKEN')
    RABBIT_USER = os.getenv('RABBIT_USER')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')
    RABBIT_URL = os.getenv('RABBIT_URL')
    REDIS_URL = os.getenv('REDIS_URL')

    ROOT_DIR = Path(__file__).absolute().parent
    APPS_DIR = ROOT_DIR.joinpath('apps')

    broker_url = f'amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_URL}'
    redis_url = f'redis://{REDIS_URL}'
    celery = Celery('tasks', broker=broker_url, backend=redis_url,)

    def __init__(self):
        assert self.TG_API_TOKEN, 'TG_API_TOKEN IS REQUIRED'
        self.bot = Bot(token=self.TG_API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.celery.conf.timezone = 'Europe/Moscow'

    def get_apps(self) -> Iterable[AppTG]:
        for i in self.APPS_DIR.iterdir():
            if i.is_dir() and i.joinpath('app.py').exists():
                yield AppTG(i)


config = Config()
