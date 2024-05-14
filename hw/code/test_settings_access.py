import time
from typing import Optional
from _pytest.fixtures import FixtureRequest
from selenium.common.exceptions import TimeoutException

from base import LoginCase
from test_settings import SettingsCase
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators
from ui.locators.settings_access import SettingsAccessPageLocators as locators
from ui.pages.settings_page import SettingsPage
from ui.pages import settings_page

from ui.fixtures import *


class SettingsAccessCase(SettingsCase):
    def change_section(self):
        self.settings_page.click(locator=locators.TAB_ITEM)

        self.settings_page.wait_until_loaded([
            locators.ADD_CABINET_BUTTON,
        ])


class TestSettingsAccess(SettingsAccessCase):
    @pytest.mark.skip('skip')
    def test_more(self):
        self.settings_page.click(locator=locators.MORE_BUTTON)

        self.settings_page.assert_window_count(2)

        print(self.settings_page.driver.current_window_handle)
        print(self.settings_page.driver.current_url)

