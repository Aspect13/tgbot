import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from apps.browser.settings import settings
from utils import Singleton


class Driver(metaclass=Singleton):
    _driver = None

    def __getattr__(self, name: str):
        return getattr(self.driver, name)

    @property
    def driver(self) -> Chrome:
        if self._driver is None:
            logging.info('Driver init')
            self._driver = Chrome(options=self.chrome_options)
        return self._driver

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
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--disable-crash-reporter")
            chrome_options.add_argument("--disable-oopr-debug-crash-dump")
            chrome_options.add_argument("--no-crash-upload")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-low-res-tiling")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent")

        if settings.mute_audio:
            chrome_options.add_argument('--mute-audio')
        return chrome_options

    # def __init__(self, *args, **kwargs):
    #     logging.info('Driver init')
    #     self._driver = Chrome(options=self.chrome_options)

    def quit(self) -> None:
        if self._driver is not None:
            self._driver.quit()
            logging.info('Driver quit')
            self._driver = None

    def __del__(self):
        self.quit()
