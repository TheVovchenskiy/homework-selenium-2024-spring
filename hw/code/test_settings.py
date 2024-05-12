import time
from typing import Optional
from _pytest.fixtures import FixtureRequest

from base import LoginCase
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators
from ui.pages.settings_page import SettingsPage
from ui.pages import settings_page

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

    # @pytest.fixture(autouse=True)
    # def save_and_restore_settings(self, request, setup):
    #     self.settings_setup()
    #     original_settings = self.settings_page.get_current_settings()

    #     self.settings_page.set_settings({
    #         'phone': settings_page.DEFAULT_PHONE,
    #         'name': settings_page.DEFAULT_NAME,
    #         'inn': settings_page.DEFAULT_INN,
    #         'cabinet': settings_page.DEFAULT_CABINET,
    #     })

    #     def restore_settings():
    #         self.settings_page.set_settings(original_settings)

    #     request.addfinalizer(restore_settings)

    def error_match(self, locator: Locator, expected_error: Optional[str]) -> bool:
        time.sleep(1)
        if expected_error is None:
            return True

        existing_error = self.settings_page.get_error(locator)

        if expected_error in existing_error.text:
            return True

        return False


class TestSettings(SettingsCase):
    @pytest.mark.skip('skip')
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

    @pytest.mark.skip('skip')
    @pytest.mark.parametrize(
        'input_data,expected_value,expected_error',
        [
            pytest.param(
                '+71234567890',
                '+71234567890',
                None,
            ),
            pytest.param(
                '+3159608363276',
                '+3159608363276',
                None,
            ),
            pytest.param(
                '+3159608363276123',
                '+3159608363276',
                None,
            ),
            pytest.param(
                '+3159608363276abc',
                '+3159608363276',
                None,
            ),
            pytest.param(
                '81234567890',
                '81234567890',
                settings_page.ERR_INVALID_PHONE_NUMBER,
            ),
            pytest.param(
                '+7123456789',
                '+7123456789',
                settings_page.ERR_INVALID_PHONE_NUMBER,
            ),
            pytest.param(
                'abc',
                'abc',
                settings_page.ERR_INVALID_PHONE_NUMBER,
            ),
        ]
    )
    def test_general_phone_input_save(
        self,
        input_data,
        expected_value,
        expected_error,
    ):
        assert not self.settings_page.save_cancel_is_visible()

        prev_phone_number, curr_value = self.settings_page.update_phone_number(
            input_data,
        )

        assert curr_value == expected_value

        assert self.settings_page.save_cancel_is_visible()

        self.settings_page.press_save()

        assert self.error_match(
            SettingsPageLocators.PHONE_BLOCK,
            expected_error,
        )

        if not expected_error:
            _, curr_value = self.settings_page.update_phone_number(
                prev_phone_number)
            self.settings_page.press_save()

            assert curr_value == prev_phone_number
        else:
            self.settings_page.press_cancel()

            assert prev_phone_number == self.settings_page.get_input_value(
                locator=SettingsPageLocators.PHONE_INPUT,
            )

        time.sleep(1)

    def test_general_email(self):
        assert not self.settings_page.save_cancel_is_visible()

        self.settings_page.press_add_email()

        assert self.settings_page.save_cancel_is_visible()

        self.settings_page.press_save()

        assert self.error_match(
            SettingsPageLocators.ADDITIONAL_EMAIL_BLOCK,
            settings_page.ERR_REQUIRED_FIELD,
        )

        for email, error in [
            ('email@example.c', settings_page.ERR_INVALID_EMAIL),
            ('email@example', settings_page.ERR_INVALID_EMAIL),
            ('email@@example.com', settings_page.ERR_INVALID_EMAIL),
            ('@example.com', settings_page.ERR_INVALID_EMAIL),
            ('email', settings_page.ERR_INVALID_EMAIL),
            ('@', settings_page.ERR_INVALID_EMAIL),
            ('email', settings_page.ERR_INVALID_EMAIL),
            ('email@example.co', None),
            ('email@example.com', None),
        ]:
            self.settings_page.update_email(0, email)
            assert self.error_match(
                SettingsPageLocators.ADDITIONAL_EMAIL_BLOCK,
                error,
            )

        self.settings_page.press_save()

        self.settings_page.has_warning('Подтвердите почту')

        self.settings_page.remove_additional_email()

        time.sleep(1)
