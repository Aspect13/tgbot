from aiogram.types import BotCommand

from apps.helper.commander import register_command

cmd_close = BotCommand(command="close", description="close browser")
register_command(cmd_close, group='browser')

cmd_goto = BotCommand(command="goto", description="go to page")
register_command(cmd_goto, group='browser')

cmd_screenshot = BotCommand(command="ss", description="make a screenshot of current page")
register_command(cmd_screenshot, group='browser')
