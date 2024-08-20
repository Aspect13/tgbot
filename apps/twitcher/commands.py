from aiogram.types import BotCommand

from apps.helper.commander import register_command

cmd_driver = BotCommand(command="driver", description="init browser driver")
register_command(cmd_driver, group='twitcher')

cmd_login = BotCommand(command="login", description="Login")
register_command(cmd_login, group='twitcher')

cmd_verification_code = BotCommand(command="vc", description="cmd_verification_code")
register_command(cmd_verification_code, group='twitcher')

cmd_save_cookies = BotCommand(command="save", description="save auth cookies")
register_command(cmd_save_cookies, group='twitcher')

cmd_watch = BotCommand(command="watch", description="go to twitch channel")
register_command(cmd_watch, group='twitcher')

cmd_bypass_mature_warning = BotCommand(command="mature_warning", description="bypass twitch warning")
register_command(cmd_bypass_mature_warning, group='twitcher')
