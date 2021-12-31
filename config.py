import os
import logging
from pathlib import Path
from typing import Iterable

from aiogram import Bot, Dispatcher

from utils import Singleton, AppBase

logging.basicConfig(level=logging.INFO)


class Config(metaclass=Singleton):
    API_TOKEN = os.getenv('API_TOKEN')

    ROOT_DIR = Path(__file__).absolute().parent
    APPS_DIR = ROOT_DIR.joinpath('apps')

    def __init__(self):
        assert self.API_TOKEN, 'API TOKEN IS REQUIRED'
        self.bot = Bot(token=self.API_TOKEN)
        self.dp = Dispatcher(self.bot)

    def get_apps(self) -> Iterable[AppBase]:
        return (AppBase(i) for i in self.APPS_DIR.iterdir() if i.is_dir() and i.joinpath('app.py').exists())


config = Config()
