import time
from typing import Optional
from selenium.common.exceptions import TimeoutException

from base import LoginCase
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators as locators
from ui.pages.settings_page import SettingsPage
from ui.pages import settings_page

from ui.fixtures import *


class SettingsCase(LoginCase):
    def settings_setup(self):
        self.settings_page = SettingsPage(self.driver)
        self.settings_page.wait_until_loaded([
            locators.PHONE_INPUT,
            locators.EMAIL_INPUT,
            locators.NAME_INPUT,
            locators.INN_INPUT,
            locators.CABINET_INPUT,
        ])

        self.change_section()

    def change_section(self):
        pass

    def error_match(self, locator: Locator, expected_error: Optional[str]) -> bool:
        if expected_error is None:
            try:
                existing_error = self.settings_page.get_error(locator, 0.5)
            except TimeoutException:
                return True
            else:
                return False

        existing_error = self.settings_page.get_error(locator, 1)

        print(existing_error.text)
        print(expected_error)
        if expected_error in existing_error.text:
            return True

        return False


class TestSettings(SettingsCase):

    @pytest.fixture
    def pre_post_check(self):
        assert self.settings_page.save_cancel_is_invisible()

        yield

        assert self.settings_page.save_cancel_is_invisible()

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
    def test_layout(self, expected_values):
        assert all(map(
            lambda item: item in self.driver.page_source,
            expected_values,
        ))

    def test_phone_input(self, pre_post_check):
        prev_phone_number = self.settings_page.get_input_value(
            locator=locators.PHONE_INPUT,
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
            prev_value, curr_value = self.settings_page.update_input_field(
                new_value,
                locator=locators.PHONE_INPUT,
            )
            assert curr_value == new_value[:14]

            if prev_value == curr_value:
                assert self.settings_page.save_cancel_is_invisible()
            else:
                assert self.settings_page.save_cancel_is_visible()
                self.settings_page.press_save(expected_error is None, 1)

                curr_value = self.settings_page.get_input_value(
                    locator=locators.PHONE_INPUT,
                )
                assert curr_value == expected_value_after_save

            assert self.error_match(
                locators.PHONE_BLOCK,
                expected_error,
            )

        self.settings_page.update_input_field(
            prev_phone_number,
            locator=locators.PHONE_INPUT,
        )

        self.settings_page.press_save()

    def test_email_input(self, pre_post_check):
        self.settings_page.press_add_email()

        assert self.settings_page.save_cancel_is_visible()

        self.settings_page.press_save()

        assert self.error_match(
            locators.ADDITIONAL_EMAIL_BLOCK(0),
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
                locators.ADDITIONAL_EMAIL_BLOCK(0),
                expected_error,
            )

        self.settings_page.press_save()

        self.settings_page.has_warning('Подтвердите почту')

        self.settings_page.remove_additional_email()

        try:
            self.settings_page.press_save(timeout=0.1)
        except TimeoutException:
            pass

    def test_name_input(self, pre_post_check):
        prev_name = self.settings_page.get_input_value(
            locator=locators.NAME_INPUT,
        )

        for new_value, expected_value_after_save, expect_save, expected_error in [
            ('Иван', 'Иван', True, None),
            ('Иван Иванович', 'Иван Иванович', True, None),
            ('Иван Иванович-Иванов', 'Иван Иванович-Иванов', True, None),
            ('Иван    Иванович     Иванов', 'Иван Иванович Иванов', True, None),
            ('  Иван Иванович Иванов  ', '  Иван Иванович Иванов  ', False,  None),
            ('и' * 256, 'и' * 255, True, None),
            ('', '', False, settings_page.ERR_REQUIRED_FIELD),
            ('    ', '    ', False, settings_page.ERR_ONLY_SPACES),
            ('Ivan', 'Ivan', False, settings_page.ERR_INVALID_NAME_SYMBOLS),
        ]:
            prev_value, curr_value = self.settings_page.update_input_field(
                new_value,
                locator=locators.NAME_INPUT,
            )

            assert curr_value == new_value[:255]

            if prev_value == curr_value:
                assert self.settings_page.save_cancel_is_invisible()
            else:
                assert self.settings_page.save_cancel_is_visible()
                self.settings_page.press_save(expect_save)

                curr_value_after_save = self.settings_page.get_input_value(
                    locator=locators.NAME_INPUT,
                )
                assert curr_value_after_save == expected_value_after_save

            assert self.error_match(
                locators.NAME_BLOCK,
                expected_error,
            )

        self.settings_page.update_input_field(
            prev_name,
            locator=locators.NAME_INPUT,
        )

        try:
            self.settings_page.press_save(timeout=0.1)
        except TimeoutException:
            pass

    def test_inn(self, pre_post_check):
        prev_inn = self.settings_page.get_input_value(
            locator=locators.INN_INPUT,
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
                assert self.settings_page.save_cancel_is_invisible()
            else:
                assert self.settings_page.save_cancel_is_visible()

                self.settings_page.press_save(expected_error is None, 1)

            assert self.error_match(
                locators.INN_BLOCK,
                expected_error,
            )

        self.settings_page.update_inn(prev_inn)

        try:
            self.settings_page.press_save(timeout=0.1)
        except TimeoutException:
            pass

    def test_cabinet_input(self, pre_post_check):
        prev_cabinet = self.settings_page.get_input_value(
            locator=locators.CABINET_INPUT,
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
                assert self.settings_page.save_cancel_is_invisible()
            else:
                assert self.settings_page.save_cancel_is_visible()

                self.settings_page.press_save(expected_error is None, 1)

            assert self.error_match(
                locators.CABINET_BLOCK,
                expected_error,
            )

        self.settings_page.update_cabinet(prev_cabinet)

        try:
            self.settings_page.press_save(timeout=0.1)
        except TimeoutException:
            pass

    def test_language(self):
        self.settings_page.change_language()

    def test_connected_cabinet(self, pre_post_check):
        self.settings_page.scroll_to_connected_cabinet()

        self.settings_page.click(locator=locators.CONNECT_CABINET)

        assert self.settings_page\
            .wait_until_visible(locators.CONNECT_CABINET_MODAL)\
            .is_displayed()

    def test_api_access(self, pre_post_check):
        self.settings_page.scroll_to(locators.API_ACCESS_BUTTON)

        self.settings_page.click(
            locator=locators.API_ACCESS_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.API_ACCESS_MODAL)\
            .is_displayed()

        name_input = self.settings_page\
            .find(
                locators.API_ACCESS_NAME_INPUT,
                locator_to_find_in=locators.API_ACCESS_MODAL,
            )
        phone_input = self.settings_page\
            .find(
                locators.API_ACCESS_PHONE_INPUT,
                locator_to_find_in=locators.API_ACCESS_MODAL,
            )
        email_input = self.settings_page\
            .find(
                locators.API_ACCESS_EMAIL_INPUT,
                locator_to_find_in=locators.API_ACCESS_MODAL,
            )

        save_button = self.settings_page\
            .find(locators.API_ACCESS_SAVE_BUTTON)
        cancel_button = self.settings_page\
            .find(
                locators.API_ACCESS_CANCEL_BUTTON,
                locator_to_find_in=locators.API_ACCESS_MODAL,
            )

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
            ('Иван    Иванович     Иванов',  None),
            ('  Иван Иванович Иванов  ',  None),
            ('    ', settings_page.ERR_API_INVALID_NAME),
        ]:
            self.settings_page.update_input_field(name, input=name_input)
            assert save_button.is_enabled()

            self.settings_page.click(elem=save_button)

            assert self.error_match(
                locators.API_ACCESS_NAME_BLOCK,
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
                locators.API_ACCESS_PHONE_BLOCK,
                expected_error,
            )

        for email, expected_error in [
            ('email@example.co', None),
            ('email@e.x.a.m.p.l.e.com', None),
            ('email@example.com',  None),
            (' mail@e.com',  None),
            ('mail@e.com ',  None),
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
            ('    ',  settings_page.ERR_API_INVALID_EMAIL),
        ]:
            self.settings_page.update_input_field(email, input=email_input)
            assert save_button.is_enabled()

            self.settings_page.click(elem=save_button)

            assert self.error_match(
                locators.API_ACCESS_EMAIL_BLOCK,
                expected_error,
            )

        self.settings_page.click(elem=cancel_button)

    def test_end_sessions(self, pre_post_check):
        self.settings_page.scroll_to(
            locators.LOGOUT_ALL_DEVICES_BUTTON)

        self.settings_page\
            .click(locator=locators.LOGOUT_ALL_DEVICES_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.LOGOUT_ALL_DEVICES_MESSAGE)\
            .is_displayed()

    def test_delete_cabinet(self, pre_post_check):
        self.settings_page.scroll_to(
            locators.DELETE_CABINET_BUTTON)

        self.settings_page\
            .click(locator=locators.DELETE_CABINET_BUTTON)

        assert self.settings_page\
            .wait_until_visible(locators.DELETE_CABINET_MODAL)\
            .is_displayed()
