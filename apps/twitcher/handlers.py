import pickle

from aiogram import types, Dispatcher, Router
from aiogram.filters import Command

from .commands import cmd_login, cmd_verification_code, cmd_save_cookies, cmd_driver
from .browser import TwitchDriver
from .settings import settings

TMP_USER_ID = 123


def init(dp: Router | Dispatcher) -> None:
    @dp.message(Command(cmd_driver))
    async def handle_init_driver(message: types.Message):
        await message.answer('Initializing driver...')
        TwitchDriver(TMP_USER_ID)
        await message.answer(f'Driver init done')

    @dp.message(Command(cmd_login))
    async def handle_login_action(message: types.Message):
        try:
            TwitchDriver(TMP_USER_ID).handle_login()
        except Exception as e:
            if 'verification' in str(e):
                await message.answer(f'{str(e)}\nUse /vc + code')
            else:
                await message.answer(str(e))
            return

        await message.answer(f'Login success')

    @dp.message(Command(cmd_verification_code))
    async def handle_verification_code(message: types.Message):
        vc = message.text.split()[1]
        driver = TwitchDriver(TMP_USER_ID)
        driver.handle_verification(vc)
        driver.skip_update_password()
        await message.answer('Code applied')

    @dp.message(Command(cmd_save_cookies))
    async def handle_save(message: types.Message):
        if settings.username:
            driver = TwitchDriver(TMP_USER_ID)
            pickle.dump(driver.get_cookies(), open(driver.cookie_file, 'wb'))
            await message.answer('cookies saved')
        else:
            await message.answer('no username provided')
