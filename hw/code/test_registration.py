from base import BaseCase
from ui.locators.registration_locators import RegistrationPageLocators
from ui.pages import registration_page

from ui.fixtures import *

REQUIRED_FIELD = "Обязательное поле"
INCORRECT_EMAIL = "Некорректный email адрес"

class TestSupportCase(BaseCase):

    def registration_setup(self):
        self.registration_page = registration_page.RegistrationPage(self.driver)

    @pytest.fixture
    def select_legal_entity(self):
        self.registration_page.set_legal_entity()

    # @pytest.mark.skip('skip')
    def test_select_country(self, select_legal_entity):
        self.registration_page.change_country(5)
    
    # @pytest.mark.skip('skip')
    def test_select_currency(self, select_legal_entity):
        self.registration_page.change_currency('RUB')

        self.registration_page.change_country(10)

    # @pytest.mark.skip('skip')
    def test_email_form(self, select_legal_entity):
        email_elem = self.registration_page.find(RegistrationPageLocators.EMAIL_INPUT)
        email_elem.clear()

        for input, expected_error in [
            ("", REQUIRED_FIELD),
            ("   ", INCORRECT_EMAIL),
            ("email.mail.ru", INCORRECT_EMAIL),
            ("email@.mail.ru", INCORRECT_EMAIL),
            ("email@mail", INCORRECT_EMAIL),
            (" example@mail.ru", INCORRECT_EMAIL),
            ("example@mail.ru ", INCORRECT_EMAIL),
        ]:
            
            self.registration_page.enter_email(input)
            self.registration_page.press_sign_up_button()

            err_locator = RegistrationPageLocators.ERROR_OF_FIELD("Email")
            try:
                err_element = self.registration_page.find(err_locator)
                assert err_element.text == expected_error
            except:
                assert expected_error == None

    # @pytest.mark.skip('skip')
    # def test_email_form_correct_input(self, select_legal_entity):
    #     email_elem = self.registration_page.find(RegistrationPageLocators.EMAIL_INPUT)
    #     email_elem.clear()
            
    #     self.registration_page.enter_email("example@mail.ru")
    #     self.registration_page.press_sign_up_button()

    #     err_locator = RegistrationPageLocators.ERROR_OF_FIELD("Email")
    #     try:
    #         self.registration_page.find(err_locator)
    #     except:
    #         assert 1 == 1
    

    
        