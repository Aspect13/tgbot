import pickle
from io import BytesIO

from aiogram import types
from aiogram.types import InputFile

from .utils import Driver
# from .app_settings import AppSettings

from config import config

dp = config.dp
# settings = AppSettings()

TMP_USER_ID = 123

@dp.message_handler(commands=['driver'])
async def handle_init_driver(message: types.Message):
    # if driver:
    #     return await message.answer('Driver already running. You may /close it')
    await message.answer('Initializing driver...')
    # try:
    #     driver = get_driver()
    #     # driver.get('https://www.twitch.tv/pestily')
    #     # handle_login(driver)
    # except Exception as e:
    #
    #     if 'verification' in str(e):
    #         await message.answer(f'{str(e)}\nUse /vc + code')
    #     else:
    #         await message.answer(str(e))
    #     return

    Driver(TMP_USER_ID).bypass_mature_warning()
    await message.answer(f'Driver init done')


@dp.message_handler(commands=['login'])
async def handle_login_action(message: types.Message):
    # if not driver:
    #     return await message.answer('Init driver with /driver')
    try:
        # handle_login(driver)
        Driver(TMP_USER_ID).handle_login()
    except Exception as e:
        if 'verification' in str(e):
            await message.answer(f'{str(e)}\nUse /vc + code')
        else:
            await message.answer(str(e))
        return

    await message.answer(f'Login success')


@dp.message_handler(commands=['vc'])
async def handle_verification_code(message: types.Message):
    # if not driver:
    #     return await message.answer('Init driver with /driver')
    vc = message.text.split()[1]
    # handle_verification(driver, message.text.split()[1])
    # skip_update_password(driver)
    driver = Driver(TMP_USER_ID)
    driver.handle_verification(vc)
    driver.skip_update_password()
    await message.answer('Code applied')


@dp.message_handler(commands=['goto'])
async def handle_goto(message: types.Message):
    # if not driver:
    #     return await message.answer('Init driver with /driver')
    try:
        url = message.text.split()[1].strip()
    except IndexError:
        return await message.answer(f'Specify URL')
    driver = Driver(TMP_USER_ID)
    driver.get(url)
    # bypass_mature_warning(driver)
    driver.bypass_mature_warning()

    await message.answer(f"Watching: {url}")


@dp.message_handler(commands=['ss'])
async def handle_screenshot(message: types.Message):
    # if not driver:
    #     return await message.answer('Init driver with /driver')
    png = Driver(TMP_USER_ID).get_screenshot_as_png()
    file = BytesIO()
    file.write(png)
    file.seek(0)

    await message.answer_photo(InputFile(file))


@dp.message_handler(commands=['save'])
async def handle_save(message: types.Message):
    # if not driver:
    #     return await message.answer('Init driver with /driver')

    # pickle.dump(driver.get_cookies(), open(settings.cookie_file, 'wb'))
    driver = Driver(TMP_USER_ID)
    pickle.dump(driver.get_cookies(), open(driver.cookie_file, 'wb'))
    await message.answer('cookies saved')


@dp.message_handler(commands=['close'])
async def handle_close(message: types.Message):
    try:
        Driver(TMP_USER_ID).close()
    finally:
        Driver.purge()
    await message.answer('closed')
