from selenium.common.exceptions import TimeoutException

from base import LoginCase
from test_settings import SettingsCase
from ui.locators.settings_notifications import SettingsNotificationsPageLocators as locators

from ui.fixtures import *


class SettingsNotificationsCase(SettingsCase):
    def disable_all_switches(self):
        if self.settings_page.find(locators.EMAIL_CHECKBOX).is_selected():
            self.settings_page.click(locator=locators.EMAIL_CHECKBOX_BUTTON)

        if self.settings_page.find(locators.NOTIFICATIONS_CHECKBOX).is_selected():
            self.settings_page\
                .click(locator=locators.NOTIFICATIONS_CHECKBOX_BUTTON)

        if self.settings_page.find(locators.TELEGRAM_CHECKBOX).is_selected():
            self.settings_page\
                .click(locator=locators.TELEGRAM_CHECKBOX_BUTTON)

    def enable_all_switches(self):
        if not self.settings_page.find(locators.EMAIL_CHECKBOX).is_selected():
            self.settings_page.click(locator=locators.EMAIL_CHECKBOX_BUTTON)

        if not self.settings_page.find(locators.NOTIFICATIONS_CHECKBOX).is_selected():
            self.settings_page.click(
                locator=locators.NOTIFICATIONS_CHECKBOX_BUTTON)

        if not self.settings_page.find(locators.TELEGRAM_CHECKBOX).is_selected():
            self.settings_page.click(locator=locators.TELEGRAM_CHECKBOX_BUTTON)

    def change_section(self):
        self.settings_page.click(locator=locators.TAB_ITEM)

        self.settings_page.wait_until_loaded([
            locators.EMAIL_CHECKBOX,
            locators.NOTIFICATIONS_CHECKBOX,
        ])


class TestSettingsNotifications(SettingsNotificationsCase):

    def test_disabled_checkboxes(self):
        self.disable_all_switches()

        assert self.settings_page\
            .find(locators.WARNING)\
            .is_displayed()

        assert len(
            self.settings_page.find_all(locators.DISABLED_CHECKBOXES)
        ) == 8

    def test_enabled_checkboxes(self):
        self.enable_all_switches()

        with pytest.raises(TimeoutException):
            self.settings_page\
                .find(locators.WARNING, timeout=0.5)\
                .is_displayed()

        with pytest.raises(TimeoutException):
            self.settings_page.find_all(
                locators.DISABLED_CHECKBOXES, timeout=0.5)
