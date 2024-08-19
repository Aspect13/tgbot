import logging
import pickle
import weakref

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from utils import Singleton
from .settings import settings, cookies_path
from ..browser.driver import Driver


class TwitchDriver(metaclass=Singleton):
    cookie_file = cookies_path.joinpath(f'{settings.username}.pkl'.lower())

    def __getattr__(self, name: str):
        return getattr(self.driver, name)

    def __init__(self, user_id: int):
        # if self.__class__._instance = weakref.proxy(self)
        logging.warning('Twitcher DRIVER INIT')
        self.user_id = user_id

        self.driver = Driver()
        self.load_cookies()
        self.driver.get('https://www.twitch.tv/')

    def load_cookies(self):
        try:
            cookies = pickle.load(open(self.cookie_file, 'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except FileNotFoundError:
            ...

    def handle_verification(self, verification_code: str = None):
        try:
            verification_inputs = WebDriverWait(self.driver, timeout=10).until(
                lambda d: d.find_elements(
                    By.CSS_SELECTOR,
                    'div[data-a-target=verification-code-input-component-input] > input'
                )
            )
            print(verification_inputs)
            if verification_inputs:
                print('VERIFICATION REQUESTED')
                if verification_code:
                    # verification_code = input('Enter verification code from email\n').strip()
                    for inp, value in zip(verification_inputs, verification_code):
                        inp.send_keys(value)
                else:
                    raise Exception('Got verification')
        except TimeoutException:
            ...

    def skip_update_password(self):
        try:
            update_password_skip = WebDriverWait(self.driver, timeout=10).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR,
                    'button[data-a-target=account-checkup-generic-modal-secondary-button]'
                )
            )
            # print(update_password_skip)
            if update_password_skip:
                update_password_skip.click()
                print('update_password skipped')

        except TimeoutException:
            ...

    def handle_login(self):
        login_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-a-target=login-button]')
        login_btn.click()

        login_input = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.ID, 'login-username'))
        password_input = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.ID, 'password-input'))

        login_input.send_keys(settings.username)
        password_input.send_keys(settings.password + Keys.RETURN)

        try:
            captcha = WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.ID, 'CaptchaFrame'))
            if captcha:
                print('We got captcha, we are fucked')
                raise Exception('Got captcha\'d')
        except TimeoutException:
            ...

        self.handle_verification()
        self.skip_update_password()

    def bypass_mature_warning(self):
        try:
            mature_warning_btn = WebDriverWait(self.driver, timeout=10).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR,
                    'button[data-a-target=player-overlay-mature-accept]'
                )
            )
            print(mature_warning_btn)
            if mature_warning_btn:
                mature_warning_btn.click()
                print('mature_warning accepted')
        except TimeoutException:
            ...
