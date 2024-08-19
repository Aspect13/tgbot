from aiogram import Router

from tg_bot import root_dispatcher
from .handlers import init


dp = Router(name='twitcher')
init(dp)
root_dispatcher.include_router(dp)
