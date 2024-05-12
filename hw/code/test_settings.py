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
        time.sleep(0.5)
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
    def test_general_phone_input_save(self):
        assert not self.settings_page.save_cancel_is_visible()

        prev_phone_number = self.settings_page.get_input_value(
            locator=SettingsPageLocators.PHONE_INPUT,
        )

        for phone_number, expected_value, expected_error in [
            ('+71234567890', '+71234567890', None),
            ('+3159608363276', '+3159608363276', None),
            ('+3159608363276123', '+3159608363276', None),
            ('+3159608363276abc', '+3159608363276', None),
            ('81234567890', '81234567890', settings_page.ERR_INVALID_PHONE_NUMBER),
            ('+7123456789', '+7123456789', settings_page.ERR_INVALID_PHONE_NUMBER),
            ('abc', 'abc', settings_page.ERR_INVALID_PHONE_NUMBER),
        ]:
            prev_value, curr_value = self.settings_page.update_phone_number(
                phone_number,
            )
            assert curr_value == expected_value

            # if prev_value == curr_value:
            #     assert not self.settings_page.save_cancel_is_visible()
            # else:
            assert self.settings_page.save_cancel_is_visible()

            self.settings_page.press_save()

            assert self.error_match(
                SettingsPageLocators.PHONE_BLOCK,
                expected_error,
            )

        self.settings_page.update_phone_number(prev_phone_number)

        self.settings_page.press_save()

        time.sleep(1)

    # @pytest.mark.skip('skip')
    def test_general_email(self):
        assert not self.settings_page.save_cancel_is_visible()

        self.settings_page.press_add_email()

        assert self.settings_page.save_cancel_is_visible()

        self.settings_page.press_save()

        assert self.error_match(
            SettingsPageLocators.ADDITIONAL_EMAIL_BLOCK,
            settings_page.ERR_REQUIRED_FIELD,
        )

        for email, expected_value, expected_error in [
            ('email@e.c', 'email@e.c', settings_page.ERR_INVALID_EMAIL),
            ('email@example', 'email@example', settings_page.ERR_INVALID_EMAIL),
            ('e@@e.com', 'e@@e.com', settings_page.ERR_INVALID_EMAIL),
            ('e@e..com', 'e@e..com', settings_page.ERR_INVALID_EMAIL),
            ('em..ail@e.com', 'em..ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('@example.com', '@example.com', settings_page.ERR_INVALID_EMAIL),
            ('email', 'email', settings_page.ERR_INVALID_EMAIL),
            ('@', '@', settings_page.ERR_INVALID_EMAIL),
            ('email', 'email', settings_page.ERR_INVALID_EMAIL),
            ('e' * 256, 'e' * 255, settings_page.ERR_INVALID_EMAIL),
            ('em<ail@e.com', 'em<ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em>ail@e.com', 'em>ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em,ail@e.com', 'em,ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em"ail@e.com', 'em"ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em:ail@e.com', 'em:ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em;ail@e.com', 'em;ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em[ail@e.com', 'em[ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em]ail@e.com', 'em]ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('em@ail@e.com', 'em@ail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('ma il@e.com', 'ma il@e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e<e.com', 'mail@e<e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e>e.com', 'mail@e>e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e,e.com', 'mail@e,e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e"e.com', 'mail@e"e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e:e.com', 'mail@e:e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e;e.com', 'mail@e;e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e[e.com', 'mail@e[e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e]e.com', 'mail@e]e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e@e.com', 'mail@e@e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e e.com', 'mail@e e.com', settings_page.ERR_INVALID_EMAIL),
            (' mail@e.com', ' mail@e.com', settings_page.ERR_INVALID_EMAIL),
            ('mail@e.com ', 'mail@e.com ', settings_page.ERR_INVALID_EMAIL),
            ('email@example.co', 'email@example.co', None),
            ('email@e.x.a.m.p.l.e.com', 'email@e.x.a.m.p.l.e.com', None),
            ('email@example.com', 'email@example.com', None),
        ]:
            prev_value, curr_value = self.settings_page.update_email(0, email)
            assert curr_value == expected_value

            if prev_value == curr_value:
                assert not self.settings_page.save_cancel_is_visible()
            else:
                assert self.settings_page.save_cancel_is_visible()

            assert self.error_match(
                SettingsPageLocators.ADDITIONAL_EMAIL_BLOCK,
                expected_error,
            )

        self.settings_page.press_save()

        self.settings_page.has_warning('Подтвердите почту')

        self.settings_page.remove_additional_email()
        self.settings_page.press_save()

        time.sleep(1)
