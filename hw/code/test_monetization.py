from base import BaseCase
from ui.locators.monetization_locators import MonetizationPageLocators
from ui.pages import monetization_page

from ui.fixtures import *

class TestMonetizationCase(BaseCase):
    def monetization_setup(self):
        self.monetization_page = monetization_page.MonetizationPage(self.driver)

    @pytest.fixture
    def top_displayed_check(self):
        assert self.monetization_page.is_top_displayed()

    @pytest.mark.skip('skip')
    def test_personal_account_button(self, top_displayed_check):
        self.monetization_page.press_personal_account_button()
        self.monetization_page.assert_window_count(2)
        self.monetization_page.driver.close()

    @pytest.mark.skip('skip')
    def test_help_button(self, top_displayed_check):
        self.monetization_page.press_help_button()
        self.monetization_page.assert_window_count(2)
        self.monetization_page.driver.close()
    
    @pytest.mark.skip('skip')
    def test_for_site_button(self, top_displayed_check):
        assert self.monetization_page.is_for_site_items_displayed()

    @pytest.mark.skip('skip')
    def test_send_button_inactive(self, top_displayed_check):
        name_elem = self.monetization_page.find(MonetizationPageLocators.NAME_INPUT)
        name_elem.clear()

        email_elem = self.monetization_page.find(MonetizationPageLocators.EMAIL_INPUT)
        email_elem.clear()
            
        self.monetization_page.enter_name("")
        self.monetization_page.enter_email("")
        
        assert not self.monetization_page.is_send_feedback_button_active()

    @pytest.mark.skip('skip')
    def test_success_sending_feedback(self, top_displayed_check):
        self.monetization_page.enter_name("   ")
        self.monetization_page.enter_email("   ")
        self.monetization_page.enter_company("VK")
        self.monetization_page.enter_position("Senior junior staff middle engineer")
        self.monetization_page.enter_comment("VK Ads")

        assert self.monetization_page.is_send_feedback_button_active()
        
        self.monetization_page.press_send_feedback_button()

        assert self.monetization_page.is_success_form_displayed()
