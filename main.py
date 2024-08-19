import asyncio
import logging

from config import get_apps
from tg_bot import root_dispatcher, bot


async def main() -> None:
    for app in get_apps():
        await app.init()

    await root_dispatcher.start_polling(bot)


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(main())
    asyncio.run(main())
