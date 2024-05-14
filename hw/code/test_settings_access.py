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


ERR_ACCOUNT_NOT_FOUND = 'Не нашли такой аккаунт. Проверьте, правильно ли введён ID'
ERR_ACCOUNT_DOES_NOT_EXIST = 'Кабинета с таким ID не существует'


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

    @pytest.fixture
    def modal(self):
        self.settings_page.click(locator=locators.ADD_CABINET_BUTTON)

        time.sleep(0.5)
        assert self.settings_page\
            .find(locators.ADD_CABINET_MODAL)\
            .is_displayed()

    @pytest.mark.skip('skip')
    def test_add_cabinet_id(self, modal):
        for id, expected_value, expected_error in [
            ('4528764518', '4528764518', ERR_ACCOUNT_DOES_NOT_EXIST),
            ('7', '7', ERR_ACCOUNT_NOT_FOUND),
            ('12345678901', '1234567890', ERR_ACCOUNT_NOT_FOUND),
            ('123abc', '123', ERR_ACCOUNT_NOT_FOUND),
        ]:
            _, curr_value = self.settings_page.update_input_field(
                id,
                locator=locators.ACCOUNT_ID_INPUT,
            )

            assert curr_value == expected_value

            self.settings_page.click(locator=locators.SAVE_BUTTON)

            assert self.error_match(
                locators.ACCOUNT_ID_BLOCK,
                expected_error,
            )

    @pytest.mark.skip('skip')
    def test_add_cabinet_checkboxes(self, modal):
        assert len(self.settings_page.find_all(locators.CHECKBOX)) == 2

        self.settings_page.click(
            locator=locators.FULL_ACCESS_RADIOBUTTON,
        )
        time.sleep(0.5)

        assert len(self.settings_page.find_all(locators.CHECKBOX)) == 2

        for button, checkbox in zip(
            self.settings_page.find_all(locators.CHECKBOX_BUTTON),
            self.settings_page.find_all(locators.CHECKBOX),
        ):
            if checkbox.is_selected():
                self.settings_page.click(elem=button)

        assert sum(map(
            lambda elem: elem.is_selected(),
            self.settings_page.find_all(locators.CHECKBOX),
        )) == 1
