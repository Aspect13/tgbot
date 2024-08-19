from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram import html, Router, Dispatcher


def init(dp: Router | Dispatcher) -> None:
    @dp.message(CommandStart(ignore_case=True, ignore_mention=True))
    async def send_welcome(message: Message):
        """
        This handler will be called when user sends `/start`
        """
        await message.answer(f'''
            Hi!, {html.bold(message.from_user.full_name)}
            Available commands are:
            /driver\t- init selenium driver
            /login\t- do login
            /vc\t-enter verification code
            /goto\t- go to page
            /ss\t- make screenshot
            /save\t- save cookies
            /close\t- de-init selenium driver
        ''')
