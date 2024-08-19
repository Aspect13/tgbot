import datetime
import pickle
from io import BytesIO

from aiogram import types, Dispatcher, Router
from aiogram.types import BufferedInputFile
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from .commands import cmd_login, cmd_verification_code, cmd_screenshot, cmd_save_cookies, cmd_close, cmd_goto, \
    cmd_driver
from .browser import Driver

TMP_USER_ID = 123


def init(dp: Router | Dispatcher) -> None:
    @dp.message(cmd_driver)
    async def handle_init_driver(message: types.Message):
        await message.answer('Initializing driver...')
        Driver(TMP_USER_ID)
        await message.answer(f'Driver init done')

    @dp.message(cmd_login)
    async def handle_login_action(message: types.Message):
        try:
            Driver(TMP_USER_ID).handle_login()
        except Exception as e:
            if 'verification' in str(e):
                await message.answer(f'{str(e)}\nUse /vc + code')
            else:
                await message.answer(str(e))
            return

        await message.answer(f'Login success')

    @dp.message(cmd_verification_code)
    async def handle_verification_code(message: types.Message):
        vc = message.text.split()[1]
        driver = Driver(TMP_USER_ID)
        driver.handle_verification(vc)
        driver.skip_update_password()
        await message.answer('Code applied')

    @dp.message(cmd_goto)
    async def handle_goto(message: types.Message):
        try:
            url = message.text.split()[1].strip()
        except IndexError:
            return await message.answer(f'Specify URL')
        driver = Driver(TMP_USER_ID)
        driver.get(url)

        await message.answer(f"Watching: {url}")

    @dp.message(cmd_screenshot)
    async def handle_screenshot(message: types.Message):
        # if not driver:
        #     return await message.answer('Init driver with /driver')
        driver: ChromiumDriver = Driver(TMP_USER_ID)
        png = driver.get_screenshot_as_png()
        file = BytesIO()
        file.write(png)
        file.seek(0)
        current_url = driver.current_url.rsplit('/', 1)[-1]
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        file_name = f'scrn_{current_url}_{timestamp}.png'
        await message.answer_photo(BufferedInputFile(png, file_name))

    @dp.message(cmd_save_cookies)
    async def handle_save(message: types.Message):
        driver = Driver(TMP_USER_ID)
        pickle.dump(driver.get_cookies(), open(driver.cookie_file, 'wb'))
        await message.answer('cookies saved')

    @dp.message(cmd_close)
    async def handle_close(message: types.Message):
        try:
            Driver(TMP_USER_ID).close()
        finally:
            Driver.purge()
        await message.answer('closed')
