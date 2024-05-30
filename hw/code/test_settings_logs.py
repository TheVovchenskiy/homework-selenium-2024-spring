import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from test_settings import SettingsCase
from ui.locators.settings_logs import SettingsLogsPageLocators as locators

from ui.fixtures import *


ERR_ACCOUNT_NOT_FOUND = 'Не нашли такой аккаунт. Проверьте, правильно ли введён ID'
ERR_ACCOUNT_DOES_NOT_EXIST = 'Кабинета с таким ID не существует'


class SettingsLogsCase(SettingsCase):
    def change_section(self):
        self.settings_page.click(locator=locators.TAB_ITEM)

        self.settings_page.wait_until_loaded([
            locators.FILTER_BUTTON,
            locators.CALENDAR_BUTTON,
        ])

    def checkboxes_checked_count(self):
        return sum(map(
            lambda elem: elem.is_selected(),
            self.settings_page.find_all(locators.CHECKBOX),
        ))


class TestSettingsLogs(SettingsLogsCase):
    @pytest.fixture
    def filters_modal(self):
        self.settings_page.click(locator=locators.FILTER_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.MODAL)\
            .is_displayed()

    def test_checkboxes_reset(self, filters_modal):
        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(locator=locators.CHECKBOX_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.RESET_BUTTON).is_displayed()

        self.settings_page.click(locator=locators.WHAT_CHANGED_BUTTON)

        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(locator=locators.CHECKBOX_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.RESET_BUTTON).is_displayed()
        assert self.settings_page\
            .wait_until_visible(locators.RESET_ALL_BUTTON).is_displayed()

        self.settings_page.click(locator=locators.RESET_BUTTON)
        assert self.checkboxes_checked_count() == 0

        self.settings_page.click(locator=locators.OBJECT_TYPE_BUTTON)
        assert self.checkboxes_checked_count() == 1

        self.settings_page.click(locator=locators.WHAT_CHANGED_BUTTON)

        self.settings_page.click(locator=locators.RESET_ALL_BUTTON)
        self.settings_page.click(locator=locators.OBJECT_TYPE_BUTTON)
        assert self.checkboxes_checked_count() == 0

    def test_save_filters(self, filters_modal):
        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(locator=locators.CHECKBOX_BUTTON)

        self.settings_page.click(locator=locators.WHAT_CHANGED_BUTTON)

        checkbox_buttons = self.settings_page\
            .find_all(locators.CHECKBOX_BUTTON)

        self.settings_page.click(locator=locators.CHECKBOX_BUTTON)

        self.settings_page.click(locator=locators.SAVE_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.RESET_ALL_BUTTON).is_displayed()

        self.settings_page.click(locator=locators.RESET_ALL_BUTTON)

        with pytest.raises(TimeoutException):
            self.settings_page.find(locators.RESET_ALL_BUTTON, timeout=0.5)

    def test_search(self, filters_modal):
        search_input = self.settings_page.find(
            locators.SEARCH_FILTER_INPUT,
            locator_to_find_in=locators.MODAL,
        )

        search_input.send_keys('кампания')

        self.settings_page.wait_until_true(lambda: len(self.settings_page.find_all(locators.CHECKBOX)) == 1)

        assert len(self.settings_page.find_all(locators.CHECKBOX)) == 1

    def test_calendar(self):
        self.settings_page.click(locator=locators.CALENDAR_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.MODAL)\
            .is_displayed()

        self.settings_page.click(locator=locators.TODAY_BUTTON)

        assert self.settings_page.wait_until_visible(locators.START_DATE_INPUT)
        assert self.settings_page.wait_until_visible(locators.END_DATE_INPUT)

        today = datetime.datetime.now().date()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday = yesterday.date()

        self.settings_page.find(locators.START_DATE_INPUT).send_keys('999999' + Keys.TAB)
        assert str(today) == self.settings_page\
            .get_input_value(locator=locators.START_DATE_INPUT)

        self.settings_page.find(locators.END_DATE_INPUT).send_keys(
            f'{yesterday.day}{yesterday.month}{yesterday.year}' + Keys.TAB)

        assert str(yesterday) == self.settings_page\
            .get_input_value(locator=locators.START_DATE_INPUT)
        assert str(today) == self.settings_page\
            .get_input_value(locator=locators.END_DATE_INPUT)
