import time
from typing import Optional
from _pytest.fixtures import FixtureRequest
from selenium.common.exceptions import TimeoutException

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

    def error_match(self, locator: Locator, expected_error: Optional[str]) -> bool:
        time.sleep(0.5)
        if expected_error is None:
            return True

        existing_error = self.settings_page.get_error(locator)

        if expected_error in existing_error.text:
            return True

        return False


class TestSettings(SettingsCase):

    @pytest.fixture
    def pre_post_check(self):
        assert not self.settings_page.save_cancel_is_visible()

        yield

        assert not self.settings_page.save_cancel_is_visible()

        time.sleep(1)

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
    def test_general_phone_input(self, pre_post_check):
        prev_phone_number = self.settings_page.get_input_value(
            locator=SettingsPageLocators.PHONE_INPUT,
        )

        for new_value, expected_value_after_save, expected_error in [
            ('+71234567890', '+71234567890', None),
            ('+3159608363276', '+3159608363276', None),
            ('+3159608363276123', '+3159608363276', None),
            ('+3159608363276abc', '+3159608363276', None),
            ('81234567890', '81234567890', settings_page.ERR_INVALID_PHONE_NUMBER),
            ('+7123456789', '+7123456789', settings_page.ERR_INVALID_PHONE_NUMBER),
            ('abc', 'abc', settings_page.ERR_INVALID_PHONE_NUMBER),
            ('a'*15, 'a'*14, settings_page.ERR_INVALID_PHONE_NUMBER),
        ]:
            prev_value, curr_value = self.settings_page.update_phone_number(
                new_value,
            )
            assert curr_value == new_value[:14]

            if prev_value == curr_value:
                assert not self.settings_page.save_cancel_is_visible()
            else:
                assert self.settings_page.save_cancel_is_visible()

            try:
                self.settings_page.press_save(expected_error is not None)
            except TimeoutError:
                pass
            else:
                curr_value = self.settings_page.get_input_value(
                    locator=SettingsPageLocators.PHONE_INPUT,
                )
                assert curr_value == expected_value_after_save

            assert self.error_match(
                SettingsPageLocators.PHONE_BLOCK,
                expected_error,
            )

        self.settings_page.update_phone_number(prev_phone_number)

        self.settings_page.press_save()

    @pytest.mark.skip('skip')
    def test_general_email_input(self, pre_post_check):
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
            _, curr_value = self.settings_page.update_email(0, email)
            assert curr_value == expected_value

            assert self.settings_page.save_cancel_is_visible()

            assert self.error_match(
                SettingsPageLocators.ADDITIONAL_EMAIL_BLOCK,
                expected_error,
            )

        self.settings_page.press_save()

        self.settings_page.has_warning('Подтвердите почту')

        self.settings_page.remove_additional_email()
        self.settings_page.press_save()

    @pytest.mark.skip('skip')
    def test_general_name_input(self, pre_post_check):
        prev_name = self.settings_page.get_input_value(
            locator=SettingsPageLocators.NAME_INPUT,
        )

        for new_value, expected_value_after_save, expected_error in [
            ('Иван', 'Иван', None),
            ('Иван Иванович', 'Иван Иванович', None),
            ('Иван Иванович-Иванов', 'Иван Иванович-Иванов', None),
            ('Иван Иванович-Иванов', 'Иван Иванович-Иванов', None),
            ('Иван    Иванович     Иванов', 'Иван Иванович Иванов', None),
            ('  Иван Иванович Иванов  ', '  Иван Иванович Иванов  ', None),
            ('и' * 256, 'и' * 255, None),
            ('', '', settings_page.ERR_REQUIRED_FIELD),
            ('    ', '    ', settings_page.ERR_ONLY_SPACES),
            ('Ivan', 'Ivan', settings_page.ERR_INVALID_NAME_SYMBOLS),
        ]:
            prev_value, curr_value = self.settings_page.update_name(
                new_value,
            )

            assert curr_value == new_value[:255]

            if prev_value == curr_value:
                assert not self.settings_page.save_cancel_is_visible()
            else:
                assert self.settings_page.save_cancel_is_visible()

            try:
                self.settings_page.press_save(expected_error is not None)
            except TimeoutError:
                pass
            else:
                curr_value = self.settings_page.get_input_value(
                    locator=SettingsPageLocators.NAME_INPUT,
                )
                assert curr_value == expected_value_after_save

            assert self.error_match(
                SettingsPageLocators.NAME_BLOCK,
                expected_error,
            )

        self.settings_page.update_name(prev_name)

        self.settings_page.press_save()

    @pytest.mark.skip('skip')
    def test_general_inn(self, pre_post_check):
        prev_inn = self.settings_page.get_input_value(
            locator=SettingsPageLocators.INN_INPUT,
        )

        for new_value, expected_error in [
            ('500100732259', None),
            ('500100732254', settings_page.ERR_INVALID_INN),
            ('5001007322', settings_page.ERR_INVALID_INN_LENGTH),
            ('inn',  settings_page.ERR_INCORRECT_INN),
            ('1' * 13, settings_page.ERR_INVALID_INN),
            ('', settings_page.ERR_REQUIRED_FIELD),
        ]:
            prev_value, curr_value = self.settings_page.update_inn(
                new_value,
            )

            assert curr_value == new_value[:12]

            if prev_value == curr_value:
                assert not self.settings_page.save_cancel_is_visible()
            else:
                assert self.settings_page.save_cancel_is_visible()

            try:
                self.settings_page.press_save(expected_error is not None)
            except TimeoutError:
                pass

            assert self.error_match(
                SettingsPageLocators.INN_BLOCK,
                expected_error,
            )

        self.settings_page.update_inn(prev_inn)

        self.settings_page.press_save()

    @pytest.mark.skip('skip')
    def test_general_cabinet_input(self, pre_post_check):
        prev_cabinet = self.settings_page.get_input_value(
            locator=SettingsPageLocators.CABINET_INPUT,
        )

        for new_value, expected_error in [
            ('Cabinet', None),
            ('Cabinet name 123', None),
            (r'Cabinet name 123 !@#$%^&*()_+{}[]>?,/.\|', None),
            ('      ', settings_page.ERR_ONLY_SPACES),
        ]:
            prev_value, curr_value = self.settings_page.update_cabinet(
                new_value,
            )

            assert curr_value == new_value[:255]

            if prev_value == curr_value:
                assert not self.settings_page.save_cancel_is_visible()
            else:
                assert self.settings_page.save_cancel_is_visible()

            try:
                self.settings_page.press_save(expected_error is not None)
            except TimeoutError:
                pass

            assert self.error_match(
                SettingsPageLocators.CABINET_BLOCK,
                expected_error,
            )

        self.settings_page.update_cabinet(prev_cabinet)

        self.settings_page.press_save()

    @pytest.mark.skip('skip')
    def test_general_language(self, pre_post_check):
        self.settings_page.change_language()
        self.settings_page.change_language()

    @pytest.mark.skip('skip')
    def test_general_connected_cabinet(self, pre_post_check):
        self.settings_page.scroll_to_connected_cabinet()

        self.settings_page.click(locator=SettingsPageLocators.CONNECT_CABINET)

        assert self.settings_page\
            .find(SettingsPageLocators.CONNECT_CABINET_MODAL)\
            .is_displayed()

    # @pytest.mark.skip('skip')
    def test_general_api_access(self, pre_post_check):
        self.settings_page.scroll_to(SettingsPageLocators.API_ACCESS_BUTTON)

        self.settings_page.click(
            locator=SettingsPageLocators.API_ACCESS_BUTTON)

        time.sleep(0.5)
        assert self.settings_page\
            .find(SettingsPageLocators.API_ACCESS_MODAL)\
            .is_displayed()

        name_input = self.settings_page\
            .find(
                SettingsPageLocators.API_ACCESS_NAME_INPUT,
                locator_to_find_in=SettingsPageLocators.API_ACCESS_MODAL,
            )
        phone_input = self.settings_page\
            .find(
                SettingsPageLocators.API_ACCESS_PHONE_INPUT,
                locator_to_find_in=SettingsPageLocators.API_ACCESS_MODAL,
            )
        email_input = self.settings_page\
            .find(
                SettingsPageLocators.API_ACCESS_EMAIL_INPUT,
                locator_to_find_in=SettingsPageLocators.API_ACCESS_MODAL,
            )

        save_button = self.settings_page\
            .find(SettingsPageLocators.API_ACCESS_SAVE_BUTTON)
        cancel_button = self.settings_page\
            .find(
                SettingsPageLocators.API_ACCESS_CANCEL_BUTTON,
                locator_to_find_in=SettingsPageLocators.API_ACCESS_MODAL,
            )

        # prev_name = self.settings_page.get_input_value(input=name_input)
        # prev_phone = self.settings_page.get_input_value(input=phone_input)
        # prev_email = self.settings_page.get_input_value(input=email_input)

        self.settings_page.update_input_field('', input=name_input)
        self.settings_page.update_input_field('', input=phone_input)
        self.settings_page.update_input_field('', input=email_input)

        assert not save_button.is_enabled()

        self.settings_page.update_input_field('  ', input=name_input)
        self.settings_page.update_input_field('  ', input=phone_input)
        self.settings_page.update_input_field('  ', input=email_input)

        assert save_button.is_enabled()

        for name, expected_error in [
            ('Иван',  None),
            ('Иван Иванович',  None),
            ('Иван Иванович-Иванов',  None),
            ('Иван Иванович-Иванов',  None),
            ('Иван    Иванович     Иванов',  None),
            ('  Иван Иванович Иванов  ',  None),
            ('    ', settings_page.ERR_API_INVALID_NAME),
        ]:
            self.settings_page.update_input_field(name, input=name_input)
            assert save_button.is_enabled()

            self.settings_page.click(elem=save_button)

            assert self.error_match(
                SettingsPageLocators.API_ACCESS_NAME_BLOCK,
                expected_error,
            )

        for phone_number, expected_error in [
            ('+71234567890', None),
            ('+3159608363276', None),
            ('+3159608363276123', settings_page.ERR_API_INCORRECT_PHONE),
            ('+3159608363276abc', settings_page.ERR_API_INCORRECT_PHONE),
            ('81234567890',  settings_page.ERR_API_INCORRECT_PHONE),
            ('+7123456789', settings_page.ERR_API_INCORRECT_PHONE),
            ('abc',  settings_page.ERR_API_INCORRECT_PHONE),
            ('  ',  settings_page.ERR_API_INVALID_PHONE),
        ]:
            self.settings_page\
                .update_input_field(phone_number, input=phone_input)
            assert save_button.is_enabled()

            self.settings_page.click(elem=save_button)

            assert self.error_match(
                SettingsPageLocators.API_ACCESS_PHONE_BLOCK,
                expected_error,
            )

        for email, expected_error in [
            ('email@example.co', None),
            ('email@e.x.a.m.p.l.e.com', None),
            ('email@example.com',  None),
            ('email@e.c', settings_page.ERR_API_INCORRECT_EMAIL),
            ('email@example', settings_page.ERR_API_INCORRECT_EMAIL),
            ('e@@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('e@e..com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em..ail@e.com', settings_page.ERR_API_INCORRECT_EMAIL),
            ('@example.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('email', settings_page.ERR_API_INCORRECT_EMAIL),
            ('@', settings_page.ERR_API_INCORRECT_EMAIL),
            ('email', settings_page.ERR_API_INCORRECT_EMAIL),
            ('em<ail@e.com', settings_page.ERR_API_INCORRECT_EMAIL),
            ('em>ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em,ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em"ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em:ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em;ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em[ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em]ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('em@ail@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('ma il@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e<e.com', settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e>e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e,e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e"e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e:e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e;e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e[e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e]e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e@e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            ('mail@e e.com',  settings_page.ERR_API_INCORRECT_EMAIL),
            (' mail@e.com',  None),
            ('mail@e.com ',  None),
            ('    ',  settings_page.ERR_API_INVALID_EMAIL),
        ]:
            self.settings_page.update_input_field(email, input=email_input)
            assert save_button.is_enabled()

            self.settings_page.click(elem=save_button)

            assert self.error_match(
                SettingsPageLocators.API_ACCESS_EMAIL_BLOCK,
                expected_error,
            )

        self.settings_page.click(elem=cancel_button)
