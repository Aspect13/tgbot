import pickle

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from .settings import Settings

settings = Settings()


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--remote-debugging-port=9222')
    # chrome_options.add_argument('--remote-debugging-address=0.0.0.0')
    chrome_options.add_argument('--mute-audio')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        cookies = pickle.load(open(settings.cookie_file, 'rb'))
        driver.get('https://www.twitch.tv/')
        for cookie in cookies:
            driver.add_cookie(cookie)
    except FileNotFoundError:
        ...

    return driver


def handle_verification(driver, verification_code: str = None):
    try:
        verification_inputs = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_elements(
                By.CSS_SELECTOR,
                'div[data-a-target=verification-code-input-component-input] > input'
            )
        )
        print(verification_inputs)
        if verification_inputs:
            print('VERIFICATION REQUESTED')
            # import pyperclip as pc

            if verification_code:
                # verification_code = input('Enter verification code from email\n').strip()
                for inp, value in zip(verification_inputs, verification_code):
                    inp.send_keys(value)
            else:
                raise Exception('Got verification')
    except TimeoutException:
        ...


def skip_update_password(driver):
    try:
        update_password_skip = WebDriverWait(driver, timeout=10).until(
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


def handle_login(driver):
    login_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-a-target=login-button]')
    login_btn.click()

    login_input = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'login-username'))
    password_input = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'password-input'))

    login_input.send_keys(settings.username)
    password_input.send_keys(settings.password + Keys.RETURN)

    try:
        captcha = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.ID, 'CaptchaFrame'))
        if captcha:
            print('We got captcha, we are fucked')
            raise Exception('Got captcha\'d')
    except TimeoutException:
        ...

    handle_verification(driver)
    skip_update_password()


def bypass_mature_warning(driver):
    try:
        mature_warning_btn = WebDriverWait(driver, timeout=10).until(
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
