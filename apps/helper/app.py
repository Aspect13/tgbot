from aiogram import types

from config import config

dp = config.dp


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply('''
        Hi!
        Available commands are:
        /driver\t- init selenium driver
        /login\t- do login
        /vc\t-enter verification code
        /goto\t- go to page
        /ss\t- make screenshot
        /save\t- save cookies
        /close\t- de-init selenium driver
    ''')


# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await message.answer(message.text)
