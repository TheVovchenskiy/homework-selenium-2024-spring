from contextlib import contextmanager


import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.main_page import MainPage
from ui.pages.login_page import LoginPage
from ui.locators.base_locators import BasePageLocators


CLICK_RETRY = 3


class BaseCase:
    driver = None

    @contextmanager
    def switch_to_window(self, current, close=False):
        for w in self.driver.window_handles:
            if w != current:
                self.driver.switch_to.window(w)
                break
        yield
        if close:
            self.driver.close()
        self.driver.switch_to.window(current)

    def login_setup(self):
        pass

    def settings_setup(self):
        pass

    def support_setup(self):
        pass

    def registration_setup(self):
        pass

    def monetization_setup(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        if config['auth']:
            self.login_setup()
        else:
            self.main_page = MainPage(driver)

        self.settings_setup()
        self.support_setup()
        self.registration_setup()
        self.monetization_setup()


class LoginCase(BaseCase):
    def login_setup(self):
        self.login_page = LoginPage(self.driver)
        self.main_page = self.login_page.login()
