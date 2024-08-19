from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import root_dir


class TwitcherSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=root_dir.joinpath('.env'),
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='twitcher_'
    )
    username: str = ''
    password: str = ''


cookies_path: Path = Path(__file__).parent.joinpath('cookies')
settings = TwitcherSettings()
