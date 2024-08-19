from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html, Router, Dispatcher

from apps.helper.commander import command_registry


def init(dp: Router | Dispatcher) -> None:
    @dp.message(CommandStart(ignore_case=True, ignore_mention=True))
    async def send_welcome(message: Message):
        """
        This handler will be called when user sends `/start`
        """

        command_list = ''
        for group in sorted(command_registry.keys()):
            group_section = f'{html.bold(group)}:\n'
            for cmd in sorted(command_registry[group], key=lambda x: x.command):
                group_section += f'\t/{cmd.command}\t\t- {cmd.description}\n'
            group_section += '\n\n'
            if group is None:
                command_list = group_section + command_list
            else:
                command_list += group_section

        response = f'Hi, {html.bold(message.from_user.full_name)}\nAvailable commands are:\n\n'
        response += command_list
        await message.answer(response)
