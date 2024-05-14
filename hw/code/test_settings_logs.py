import time
from typing import Optional
from _pytest.fixtures import FixtureRequest
from selenium.common.exceptions import TimeoutException

from base import LoginCase
from test_settings import SettingsCase
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators
from ui.locators.settings_logs import SettingsLogsPageLocators as locators
from ui.pages.settings_page import SettingsPage
from ui.pages import settings_page

from ui.fixtures import *


ERR_ACCOUNT_NOT_FOUND = 'Не нашли такой аккаунт. Проверьте, правильно ли введён ID'
ERR_ACCOUNT_DOES_NOT_EXIST = 'Кабинета с таким ID не существует'


class SettingsLogsCase(SettingsCase):
    def change_section(self):
        self.settings_page.click(locator=locators.TAB_ITEM)

        self.settings_page.wait_until_loaded([
            locators.FILTER_BUTTON,
        ])

    def checkboxes_checked_count(self):
        return sum(map(
            lambda elem: elem.is_selected(),
            self.settings_page.find_all(locators.CHECKBOX),
        ))


class TestSettingsLogs(SettingsLogsCase):
    @pytest.fixture
    def filters_modal(self):
        # try:
        #     if self.settings_page\
        #         .find(locators.RESET_ALL_BUTTON, timeout=1)\
        #             .is_displayed():
        #         self.settings_page.click(locators.RESET_ALL_BUTTON)
        # except TimeoutException:
        #     pass

        self.settings_page.click(locator=locators.FILTER_BUTTON)

        time.sleep(0.5)
        assert self.settings_page\
            .find(locators.FILTER_MODAL)\
            .is_displayed()

    @pytest.mark.skip('skip')
    def test_checkboxes_reset(self, filters_modal):
        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(elem=checkbox_buttons[0])

        assert self.settings_page\
            .find(locators.RESET_BUTTON).is_displayed()

        self.settings_page.click(locator=locators.WHAT_CHANGED_BUTTON)

        time.sleep(0.5)
        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(elem=checkbox_buttons[0])

        assert self.settings_page\
            .find(locators.RESET_BUTTON).is_displayed()
        assert self.settings_page\
            .find(locators.RESET_ALL_BUTTON).is_displayed()

        self.settings_page.click(locator=locators.RESET_BUTTON)
        assert self.checkboxes_checked_count() == 0

        self.settings_page.click(locator=locators.OBJECT_TYPE_BUTTON)
        assert self.checkboxes_checked_count() == 1

        self.settings_page.click(locator=locators.WHAT_CHANGED_BUTTON)

        self.settings_page.click(locator=locators.RESET_ALL_BUTTON)
        self.settings_page.click(locator=locators.OBJECT_TYPE_BUTTON)
        assert self.checkboxes_checked_count() == 0

    @pytest.mark.skip('skip')
    def test_save_filters(self, filters_modal):
        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(elem=checkbox_buttons[0])

        self.settings_page.click(locator=locators.WHAT_CHANGED_BUTTON)

        time.sleep(0.5)
        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(elem=checkbox_buttons[0])

        self.settings_page.click(locator=locators.SAVE_BUTTON)

        assert self.settings_page\
            .find(locators.RESET_ALL_BUTTON).is_displayed()

        self.settings_page.click(locator=locators.RESET_ALL_BUTTON)

        with pytest.raises(TimeoutException):
            self.settings_page.find(locators.RESET_ALL_BUTTON, timeout=0.5)

    @pytest.mark.skip('skip')
    def test_search(self, filters_modal):
        search_input = self.settings_page.find(
            locators.SEARCH_FILTER_INPUT,
            locator_to_find_in=locators.FILTER_MODAL,
        )

        search_input.send_keys('кампания')

        assert len(self.settings_page.find_all(locators.CHECKBOX)) == 1

    # @pytest.mark.skip('skip')
    def test_calendar(self):
        pass
