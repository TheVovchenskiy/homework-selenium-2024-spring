from typing import Any
from selenium.webdriver.common.by import By


Locator = tuple[str, Any | None]


class BasePageLocators:
    CABINET_LOCATOR = (By.XPATH, '//*[contains(@class, "ButtonCabinet_primary")]')

def locator_xpath_parent(locator: Locator, step_count: int = 1) -> Locator:
    return (By.XPATH, locator[1] + '/' + '/'.join(['..'] * step_count))
