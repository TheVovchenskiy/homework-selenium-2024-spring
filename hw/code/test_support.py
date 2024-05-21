from base import BaseCase
from ui.locators.support_locators import SupportPageLocators
from ui.pages import support_page

from ui.fixtures import *

EMPTY_FORM = "Обязательное поле"
EMPTY_FORM_WITH_DOT = "Обязательное поле."
MESSAGE_IS_TOO_LONG = "Убедитесь, что это значение содержит не более 1000 символов"
NAME_IS_TOO_LONG = "Максимальная длина 30 символов"
INCORRECT_EMAIL = "Некорректный email адрес"

class TestSupportCase(BaseCase):

    def support_setup(self):
        self.support_page = support_page.SupportPage(self.driver)

    @pytest.fixture
    def open_support_window(self):
        self.support_page.click(locator=SupportPageLocators.SUPPORT_BUTTON)
        self.support_page.click(locator=SupportPageLocators.ASK_QUESTION_BUTTON)
        self.support_page.wait_until_loaded([SupportPageLocators.TOPIC_BUTTON, SupportPageLocators.MESSAGE_FORM,
                                             SupportPageLocators.NAME_FORM, SupportPageLocators.EMAIL_FORM])
    
    @pytest.mark.skip('skip')
    def test_close_button(self, open_support_window):
        assert self.support_page.is_support_window_displayed()
        self.support_page.press_close_button()
        assert self.support_page.is_support_window_hidden()

    @pytest.mark.skip('skip')
    def test_cancel_button(self, open_support_window):
        assert self.support_page.is_support_window_displayed()
        self.support_page.press_cancel_button()
        assert self.support_page.is_support_window_hidden()

    @pytest.mark.skip('skip')
    def test_faq_href(self, open_support_window):
        self.support_page.click_faq_href()
        self.support_page.assert_window_count(2)
        self.support_page.driver.close()

    @pytest.mark.skip('skip')
    def test_change_topic(self, open_support_window):
        self.support_page.change_topic("statistics")

    @pytest.mark.skip('skip')
    def test_message_form_1(self, open_support_window):
        for input, expected_error in [
            ("", EMPTY_FORM),
            ("Сообщение", None),
            ("1"*1050, None)
        ]:
            self.support_page.enter_message(input)
            self.support_page.press_submit_button()

            err_locator = SupportPageLocators.ERROR_OF_FIELD("Сообщение")
            try:
                err_element = self.support_page.find(err_locator)
                assert err_element.text == expected_error
            except:
                assert expected_error == None

    @pytest.mark.skip('skip')
    def test_message_form_2(self, open_support_window):
        self.support_page.change_topic("payments")
        self.support_page.enter_name("Имя Фамилия")

        email_elem = self.support_page.find(SupportPageLocators.EMAIL_FORM)
        email_elem.clear()
        self.support_page.enter_email("email@mail.ru")

        for input, expected_error in [
            ("    ", EMPTY_FORM_WITH_DOT),
            ("1"*1050, MESSAGE_IS_TOO_LONG)
        ]:
            self.support_page.enter_message(input)
            self.support_page.press_submit_button()
            err_locator = SupportPageLocators.ERROR_OF_FIELD("Сообщение")
            try:
                err_element = self.support_page.find(err_locator)
                assert err_element.text == expected_error
            except:
                assert expected_error == None

    @pytest.mark.skip('skip')
    def test_name_form(self, open_support_window):
        for input, expected_error in [
            ("", EMPTY_FORM),
            ("Имя Фамилия", None),
            ("1"*35, NAME_IS_TOO_LONG),
            ("    ", None)
        ]:
            self.support_page.enter_name(input)
            self.support_page.press_submit_button()

            err_locator = SupportPageLocators.ERROR_OF_FIELD("Ваше имя")
            try:
                err_element = self.support_page.find(err_locator)
                assert err_element.text == expected_error
            except:
                assert expected_error == None

    @pytest.mark.skip('skip')
    def test_email_form(self, open_support_window):
        email_elem = self.support_page.find(SupportPageLocators.EMAIL_FORM)
        email_elem.clear()

        for input, expected_error in [
            ("", EMPTY_FORM),
            ("email.@mail.ru", INCORRECT_EMAIL),
            ("email.mail.ru", INCORRECT_EMAIL),
            ("email@.mail.ru", INCORRECT_EMAIL),
            ("email@mail", INCORRECT_EMAIL),
            ("     ", INCORRECT_EMAIL),
            (" example@mail.ru", INCORRECT_EMAIL),
            ("example@mail.ru ", INCORRECT_EMAIL),
            ("example@mail.ru", None)
        ]:
            
            self.support_page.enter_email(input)
            self.support_page.press_submit_button()

            err_locator = SupportPageLocators.ERROR_OF_FIELD("Эл. почта для связи")
            try:
                err_element = self.support_page.find(err_locator)
                assert err_element.text == expected_error
            except:
                assert expected_error == None

    @pytest.mark.skip('skip')
    def test_success_case(self, open_support_window):
        email_elem = self.support_page.find(SupportPageLocators.EMAIL_FORM)
        email_elem.clear()

        self.support_page.change_topic("statistics")
        self.support_page.enter_message("Test Message")
        self.support_page.enter_name("Name Surname")
        self.support_page.enter_email("test@mail.ru")

        self.support_page.press_submit_button()

        assert self.support_page.is_success_window_displayed()
