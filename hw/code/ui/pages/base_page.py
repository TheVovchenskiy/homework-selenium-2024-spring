import time
from typing import Any, Callable, Optional

import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from ui.locators.base_locators import Locator
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


from ui.fixtures import *


TIMEOUT_UNTIL_LOADED = 15
DEFAULT_TIMEOUT = 5

MAX_RETRIES_COUNT = 3

VALUE_ATTRIBUTE_NAME = 'value'


def validate_only_one_is_not_none(*args: Any):
    if sum(map(lambda x: bool(x), args)) != 1:
        raise TypeError('one of two positional arguments must be None')


class BasePage:
    url = 'https://ads.vk.com/'

    def is_opened(self, url: Optional[str] = None, timeout: int | float = TIMEOUT_UNTIL_LOADED):
        if url is None:
            url = self.url

        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == url:
                return True
        raise TimeoutException(
            f'{url} did not open in {timeout} sec, '
            'current url {self.driver.current_url}'
        )

    def wait_until_loaded(self, locators: list[Locator], timeout=TIMEOUT_UNTIL_LOADED):
        for locator in locators:
            self.wait(TIMEOUT_UNTIL_LOADED).until(
                EC.presence_of_all_elements_located(locator)
            )

    def wait_until_visible(
        self,
        locator: Locator,
        timeout=DEFAULT_TIMEOUT,
    ) -> WebElement:
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def __init__(self, driver):
        self.driver: webdriver.Chrome = driver
        self.actions = ActionChains(self.driver)
        self.driver.get(self.url)
        self.is_opened()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout, ignored_exceptions=(StaleElementReferenceException,))

    def wait_until_true(self, func: Callable[[Any], bool], timeout: float = None, *args, **kwargs) -> bool:
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        started = time.time()
        while time.time() - started < timeout:
            if func(*args, **kwargs):
                return True

        raise TimeoutError

    def assert_window_count(self, window_count: int, timeout=DEFAULT_TIMEOUT):
        self.wait(timeout).until(EC.number_of_windows_to_be(window_count))

        assert len(self.driver.window_handles) == window_count

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
    def click(
        self,
        *,
        locator: Locator = None,
        elem: WebElement = None,
        timeout=None,
    ):
        validate_only_one_is_not_none(elem, locator)
        if elem is None:
            elem = self.find(locator, timeout=timeout)
        self.wait(timeout).until(EC.element_to_be_clickable(elem)).click()

    def update_input_field(
        self,
        new_input_data: str,
        *,
        locator: Locator = None,
        input: WebElement = None,
    ) -> tuple[str, str]:
        validate_only_one_is_not_none(locator, input)
        if input is None:
            input = self.find(locator, timeout=DEFAULT_TIMEOUT)

        prev_data = self.get_input_value(input=input)

        if new_input_data:
            input.clear()
            input.send_keys(new_input_data)
        else:
            input.send_keys(Keys.BACKSPACE * len(prev_data))

        return prev_data, self.get_input_value(input=input)

    def get_input_value(self, *, locator: Locator = None, input: WebElement = None) -> str:
        """
        Returns value of input field by given locator or by WebElement input.
        One of two params must be None.
        """
        validate_only_one_is_not_none(locator, input)
        if locator:
            input = self.find(locator, timeout=DEFAULT_TIMEOUT)

        return self.wait().until(EC.visibility_of(input)).get_attribute(VALUE_ATTRIBUTE_NAME)

    def scroll_to(self, locator: Locator):
        target_elem = self.find(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            target_elem,
        )
