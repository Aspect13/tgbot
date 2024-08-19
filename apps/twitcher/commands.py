from aiogram.filters import Command
from aiogram.types import BotCommand

cmd_login = Command(BotCommand(command="login", description="Login"))
cmd_verification_code = Command(BotCommand(command="vc", description="cmd_verification_code"))
cmd_goto = Command(BotCommand(command="goto", description="go to another page"))
cmd_screenshot = Command(BotCommand(command="ss", description="make a screenshot of current page"))
cmd_save_cookies = Command(BotCommand(command="save", description="save auth cookies"))
cmd_close = Command(BotCommand(command="close", description="close browser"))
cmd_driver = Command(BotCommand(command="driver", description="init browser driver"))
