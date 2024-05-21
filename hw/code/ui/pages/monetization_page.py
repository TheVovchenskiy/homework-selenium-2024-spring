from ui.pages.base_page import DEFAULT_TIMEOUT
from ui.locators.base_locators import Locator
from ui.locators.monetization_locators import MonetizationPageLocators
from ui.pages.base_page import BasePage


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

class MonetizationPage(BasePage):
    url = 'https://ads.vk.com/partner'

    def press_help_button(self):
        elem = self.find(MonetizationPageLocators.HELP_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_personal_account_button(self):
        elem = self.find(MonetizationPageLocators.PERSONAL_ACCOUNT_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_personal_account_button_2(self):
        elem = self.find(MonetizationPageLocators.PERSONAL_ACCOUNT_BUTTON_2)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_for_sites_button(self):
        elem = self.find(MonetizationPageLocators.FOR_SITES_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
    
    def press_for_applications_button(self):
        elem = self.find(MonetizationPageLocators.FOR_APPLICATIONS_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_send_feedback_button(self):
        elem = self.find(MonetizationPageLocators.SEND_FEEDBACK_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem))
        self.driver.execute_script("arguments[0].click();", elem)

    def is_send_feedback_button_active(self):
        return self.wait().until(EC.visibility_of_element_located(MonetizationPageLocators.SEND_FEEDBACK_BUTTON)).is_enabled()

    def is_top_displayed(self):
        return self.wait().until(EC.visibility_of_element_located(
                MonetizationPageLocators.TOP)).is_displayed()
    
    def is_for_site_items_displayed(self):
        for item in MonetizationPageLocators.FOR_SITE_ITEMS:
            if not self.wait().until(EC.visibility_of_element_located(item)).is_displayed():
                return False
            
        return True
    
    def is_for_applications_items_displayed(self):
        for item in MonetizationPageLocators.FOR_APPLICATIONS_ITEMS:
            if not self.wait().until(EC.visibility_of_element_located(item)).is_displayed():
                return False
            
        return True
    
    def enter_name(self, name):
        return self.update_input_field(
            name,
            locator=MonetizationPageLocators.NAME_INPUT,
        )

    def enter_email(self, email):
        return self.update_input_field(
            email,
            locator=MonetizationPageLocators.EMAIL_INPUT,
        )
    
    def enter_company(self, company):
        return self.update_input_field(
            company,
            locator=MonetizationPageLocators.COMPANY_INPUT,
        )
    
    def enter_position(self, position):
        return self.update_input_field(
            position,
            locator=MonetizationPageLocators.POSITION_INPUT,
        )
    
    def enter_comment(self, comment):
        return self.update_input_field(
            comment,
            locator=MonetizationPageLocators.COMMENT_INPUT,
        )
    
    def is_success_form_displayed(self):
        return self.wait().until(EC.visibility_of_element_located(MonetizationPageLocators.SUCCESS_FORM)).is_displayed()
