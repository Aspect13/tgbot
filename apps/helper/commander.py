from collections import defaultdict
from typing import Optional

from aiogram.types import BotCommand

command_registry = defaultdict(list)


def register_command(cmd: BotCommand, group: Optional[str] = None) -> None:
    command_registry[group].append(cmd)
