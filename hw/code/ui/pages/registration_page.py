import time
from ui.pages.base_page import DEFAULT_TIMEOUT
from ui.locators.base_locators import Locator
from ui.locators.registration_locators import RegistrationPageLocators
from ui.pages.base_page import BasePage


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

class RegistrationPage(BasePage):
    url = 'https://ads.vk.com/hq/registration/new'

    def click_to_background(self):
        back_elem = self.find(RegistrationPageLocators.BACKGROUND)
        back_elem.click()

    def open_country_dropdown(self):
        elem = self.find(RegistrationPageLocators.COUNTRY_BUTTON)

        id = elem.get_attribute('aria-owns')

        self.wait().until(EC.element_to_be_clickable(elem)).click()
        self.wait().until(EC.visibility_of_element_located(
            RegistrationPageLocators.COUNTRY_DROPDOWN(id)
        ))
        return id
    
    def change_country(self, num):
        id = self.open_country_dropdown()

        self.click(locator=RegistrationPageLocators.COUNTRY_ITEM(id, num))
        time.sleep(1)

        new_id = self.open_country_dropdown()

        assert self.wait().until(EC.visibility_of_element_located(
                RegistrationPageLocators.COUNTRY_ITEM(new_id, num)
        )).is_displayed()

    def open_currency_dropdown(self):
        elem = self.find(RegistrationPageLocators.CURRENCY_BUTTON)

        id = elem.get_attribute('aria-owns')

        self.wait().until(EC.element_to_be_clickable(elem)).click()
        self.wait().until(EC.visibility_of_element_located(
            RegistrationPageLocators.CURRENCY_DROPDOWN(id)
        ))
        return id
    
    def change_currency(self, name):
        id = self.open_currency_dropdown()

        self.click(locator=RegistrationPageLocators.CURRENCY_ITEM(id, name))
        time.sleep(1)

        new_id = self.open_currency_dropdown()

        assert self.wait().until(EC.visibility_of_element_located(
                RegistrationPageLocators.CURRENCY_ITEM(new_id, name)
        )).is_displayed()

    def enter_email(self, email):
        return self.update_input_field(
            email,
            locator=RegistrationPageLocators.EMAIL_INPUT,
        )
        
    def get_error(self, locator: Locator = None) -> WebElement:
        return self.find(
            RegistrationPageLocators.ERROR_MESSAGE,
            locator_to_find_in=locator,
        )
    
    def set_legal_entity(self):
        elem = self.find(RegistrationPageLocators.LEGAL_ENTITY_RADIO_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

        #assert self.wait().until(EC.visibility_of_element_located(
        #        RegistrationPageLocators.LEGAL_ENTITY_INPUT
        #)).is_selected()

    def enable_offer_checkbox(self):
        elem = self.find(RegistrationPageLocators.OFFER_CHECKBOX_TO_CLICK)
        checkbox_elem = self.find(RegistrationPageLocators.OFFER_CHECKBOX_TO_CHECK)
        is_selected = self.wait().until(EC.element_to_be_clickable(checkbox_elem)).is_selected()

        if is_selected:
            return
        else:
            elem.click()

    def click_offer_checkbox(self, enable: bool):
        elem = self.find(RegistrationPageLocators.OFFER_CHECKBOX_TO_CLICK)
        checkbox_elem = self.find(RegistrationPageLocators.OFFER_CHECKBOX_TO_CHECK)
        is_selected = self.wait().until(EC.element_to_be_clickable(checkbox_elem)).is_selected()

        if ((not enable) and is_selected) or (enable and (not is_selected)):
            elem.click()

    def press_sign_up_button(self):
        elem = self.find(RegistrationPageLocators.SIGN_UP_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()