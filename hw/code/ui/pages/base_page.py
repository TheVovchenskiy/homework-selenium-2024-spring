import time
from typing import Optional

import allure
from selenium.webdriver.remote.webelement import WebElement
from ui.locators import base_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from ui.fixtures import *


TIMEOUT_UNTIL_LOADED = 5


class PageNotOpenedExeption(Exception):
    pass


class BasePage:

    locators = base_locators.BasePageLocators()
    url = 'https://ads.vk.com/'

    def is_opened(self, url: Optional[str] = None, timeout: int | float = 15):
        if url is None:
            url = self.url

        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == url:
                return True
        raise PageNotOpenedExeption(
            f'{url} did not open in {timeout} sec, '
            'current url {self.driver.current_url}'
        )

    def wait_until_loaded(self, locators: list, timeout=TIMEOUT_UNTIL_LOADED):
        for locator in locators:
            self.wait(TIMEOUT_UNTIL_LOADED).until(
                EC.presence_of_all_elements_located(locator)
            )

    def __init__(self, driver):
        self.driver = driver
        self.is_opened()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step("Step 1")
    def my_assert(self):
        assert 1 == 1

    @allure.step('Click')
    def click(self, locator, timeout=None) -> WebElement:
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()
