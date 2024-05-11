from typing import Any
from selenium.webdriver.common.by import By


Locator = tuple[str, Any | None]


class BasePageLocators:
    CABINET_LOCATOR = (By.CLASS_NAME, 'ButtonCabinet_primary__LCfol')
