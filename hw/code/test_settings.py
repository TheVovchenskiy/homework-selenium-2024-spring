import time
from _pytest.fixtures import FixtureRequest

from base import LoginCase
from ui.locators.settings_locators import SettingsPageLocators
from ui.pages.settings_page import SettingsPage

from ui.fixtures import *


class SettingsCase(LoginCase):
    def settings_setup(self):
        self.main_page.go_to_settings()
        self.settings_page = SettingsPage(self.driver)
        self.settings_page.wait_until_loaded([
            SettingsPageLocators.PHONE_INPUT,
            SettingsPageLocators.EMAIL_INPUT,
            SettingsPageLocators.NAME_INPUT,
            SettingsPageLocators.INN_INPUT,
            SettingsPageLocators.CABINET_INPUT,
        ])


class TestSettings(SettingsCase):
    @pytest.mark.parametrize(
        'expected_values',
        [pytest.param([
            'Общие',
            'Контакты',
            'Реквизиты',
            'Интерфейс',
            'Доступ к API',
            'Выйти из других устройств',
            'Удалить кабинет',
        ])]
    )
    def test_general_layout(self, expected_values):
        assert all(
            map(lambda item: item in self.driver.page_source, expected_values)
        )
