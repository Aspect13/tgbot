import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from apps.browser.settings import settings
from utils import Singleton


class Driver(metaclass=Singleton):
    def __getattr__(self, name: str):
        return getattr(self.driver, name)

    @property
    def chrome_options(self):
        chrome_options = Options()
        if settings.headless:
            chrome_options.add_argument('--headless')

        if settings.debugger:
            chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_argument('--remote-debugging-address=0.0.0.0')

        if settings.optimizations:
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        if settings.mute_audio:
            chrome_options.add_argument('--mute-audio')
        return chrome_options

    def __init__(self, *args, **kwargs):
        logging.info('Driver init')
        self._driver = Chrome(options=self.chrome_options)

    def quit(self) -> None:
        self._driver.quit()
        self.__class__.purge()

    def __del__(self):
        self.quit()
