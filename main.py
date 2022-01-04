import asyncio

from aiogram import executor

from config import config










for app in config.get_apps():
    app.init()




if __name__ == '__main__':
    asyncio.set_event_loop(asyncio.new_event_loop())
    executor.start_polling(config.dp, skip_updates=True)
