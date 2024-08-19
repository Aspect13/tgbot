from pydantic_settings import BaseSettings, SettingsConfigDict

from config import root_dir


class BrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=root_dir.joinpath('.env'),
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='browser_'
    )
    headless: bool = True
    debugger: bool = False
    optimizations: bool = True
    mute_audio: bool = True


settings = BrowserSettings()
