import pickle
from io import BytesIO

from aiogram import types
from aiogram.types import InputMediaPhoto, InputFile

from .actions import get_driver, handle_login, bypass_mature_warning, handle_verification, skip_update_password
from .settings import Settings

from config import config

dp = config.dp
driver = None
settings = Settings()


@dp.message_handler(commands=['driver'])
async def handle_init_driver(message: types.Message):
    global driver
    if driver:
        return await message.answer('Driver already running. You may /close it')
    await message.answer('Initializing driver...')
    try:
        driver = get_driver()
        driver.get('https://www.twitch.tv/pestily')
        # handle_login(driver)
    except Exception as e:

        if 'verification' in str(e):
            await message.answer(f'{str(e)}\nUse /vc + code')
        else:
            await message.answer(str(e))
        return

    bypass_mature_warning(driver)
    await message.answer(f'Driver init done')


@dp.message_handler(commands=['login'])
async def handle_login_action(message: types.Message):
    if not driver:
        return await message.answer('Init driver with /driver')
    try:
        handle_login(driver)
    except Exception as e:
        if 'verification' in str(e):
            await message.answer(f'{str(e)}\nUse /vc + code')
        else:
            await message.answer(str(e))
        return

    await message.answer(f'Login success')


@dp.message_handler(commands=['vc'])
async def handle_verification_code(message: types.Message):
    if not driver:
        return await message.answer('Init driver with /driver')
    handle_verification(driver, message.text.strip('/vc '))
    skip_update_password(driver)
    await message.answer('Code applied')


@dp.message_handler(commands=['goto'])
async def handle_goto(message: types.Message):
    if not driver:
        return await message.answer('Init driver with /driver')
    if not message.text.strip('/goto'):
        return await message.answer(f'Specify URL')
    driver.get(message.text.strip('/goto'))
    bypass_mature_warning(driver)
    await message.answer(f"Watching: {message.text.strip('/goto')}")


@dp.message_handler(commands=['ss'])
async def handle_screenshot(message: types.Message):
    if not driver:
        return await message.answer('Init driver with /driver')
    file = BytesIO()
    file.write(driver.get_screenshot_as_png())
    file.seek(0)

    await message.answer_photo(InputFile(file))


@dp.message_handler(commands=['save'])
async def handle_save(message: types.Message):
    if not driver:
        return await message.answer('Init driver with /driver')
    pickle.dump(driver.get_cookies(), open(settings.cookie_file, 'wb'))
    await message.answer('cookies saved')


@dp.message_handler(commands=['close'])
async def handle_close(message: types.Message):
    global driver
    if driver:
        driver.close()
    driver = None
    await message.answer('closed')
