import logging
from datetime import datetime, timezone
from io import BytesIO

from aiogram import Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from .commands import cmd_close, cmd_screenshot, cmd_goto
from .driver import Driver


def init(dp: Router | Dispatcher) -> None:
    @dp.message(Command(cmd_close))
    async def handle_close(message: Message):
        try:
            Driver().quit()
        except Exception as e:
            logging.warning(e)
        await message.answer('Driver quit')

    @dp.message(Command(cmd_screenshot))
    async def handle_screenshot(message: Message):
        driver: ChromiumDriver = Driver()
        png = driver.get_screenshot_as_png()

        # file = BytesIO()
        # file.write(png)
        # file.seek(0)

        current_url = driver.current_url.rsplit('/', 1)[-1]
        timestamp = datetime.now(timezone.utc)
        file_name = f'scrn_{current_url}_{timestamp}.png'
        await message.answer_photo(BufferedInputFile(png, file_name))

    @dp.message(Command(cmd_goto))
    async def handle_goto(message: Message):
        try:
            url = message.text.split()[1].strip()
        except IndexError:
            return await message.answer(f'Specify URL')
        Driver().get(url)

        await message.answer(f"Now on url: {url}")

