import time
from typing import Optional

import allure
from selenium.webdriver.remote.webelement import WebElement
from ui.locators.base_locators import Locator
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from ui.fixtures import *


TIMEOUT_UNTIL_LOADED = 5
DEFAULT_TIMEOUT = 5


class PageNotOpenedExeption(Exception):
    pass


class BasePage:

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

    def wait_until_loaded(self, locators: list[Locator], timeout=TIMEOUT_UNTIL_LOADED):
        for locator in locators:
            self.wait(TIMEOUT_UNTIL_LOADED).until(
                EC.presence_of_all_elements_located(locator)
            )

    def __init__(self, driver):
        self.driver = driver
        self.is_opened()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def find(
            self,
            locator: Locator,
            *,
            locator_to_find_in: Locator = None,
            timeout=None,
    ) -> WebElement:
        if locator_to_find_in:
            elem_to_find_in = self.find(locator_to_find_in, timeout=timeout)
            return self.wait(timeout).until(lambda _: elem_to_find_in.find_element(*locator))
        else:
            return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_all(
        self,
        locator: Locator,
        *,
        locator_to_find_in: Locator = None,
        timeout=None,
    ) -> list[WebElement]:
        if locator_to_find_in:
            elem_to_find_in = self.find(locator_to_find_in, timeout=timeout)
            return self.wait(timeout).until(lambda _: elem_to_find_in.find_elements(*locator))
        else:
            return self.wait(timeout).until(EC.presence_of_all_elements_located(locator))

    @allure.step("Step 1")
    def my_assert(self):
        assert 1 == 1

    @allure.step('Click')
    def click(self, locator: Locator, timeout=None):
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    def update_input_field(
        self,
        locator: Locator,
        new_input_data: str,
    ) -> tuple[str, str]:
        input = self.find(locator, timeout=DEFAULT_TIMEOUT)
        prev_data = self.get_input_value(input=input)

        input.clear()
        input.send_keys(new_input_data)

        time.sleep(0.5)
        return prev_data, self.get_input_value(input=input)

    def get_input_value(self, *, locator: Locator = None, input: WebElement = None) -> str:
        if locator:
            input = self.find(locator, timeout=DEFAULT_TIMEOUT)
        return input.get_attribute('value')
