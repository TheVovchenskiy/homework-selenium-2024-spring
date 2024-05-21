import time
from ui.pages.base_page import DEFAULT_TIMEOUT
from ui.locators.base_locators import Locator
from ui.locators.support_locators import SupportPageLocators
from ui.pages.base_page import BasePage


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

class SupportPage(BasePage):
    url = 'https://ads.vk.com/hq/partner'

    def is_support_window_displayed(self):
        return self.wait().until(EC.visibility_of_element_located(SupportPageLocators.MODAL_WINDOW)).is_displayed()

    def is_support_window_hidden(self):
        return self.wait().until(EC.invisibility_of_element_located(SupportPageLocators.MODAL_WINDOW))
    
    def is_success_window_displayed(self):
        return self.wait().until(EC.visibility_of_element_located(SupportPageLocators.SUCCESS_MODAL_WINDOW)).is_displayed()

    def click_faq_href(self):
        elem = self.find(SupportPageLocators.FAQ_HREF)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_close_button(self):
        elem = self.find(SupportPageLocators.CLOSE_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
        modal_window_elem = self.find(SupportPageLocators.MODAL_WINDOW)
        self.wait().until(EC.invisibility_of_element(modal_window_elem))

    def press_cancel_button(self):
        elem = self.find(SupportPageLocators.CANCEL_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
        modal_window_elem = self.find(SupportPageLocators.MODAL_WINDOW)
        self.wait().until(EC.invisibility_of_element(modal_window_elem))

    def press_submit_button(self):
        elem = self.find(SupportPageLocators.SUMBIT_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def open_topic_dropdown(self):
        elem = self.find(SupportPageLocators.TOPIC_BUTTON)

        id = elem.get_attribute('aria-owns')

        self.wait().until(EC.element_to_be_clickable(elem)).click()
        self.wait().until(EC.visibility_of_element_located(
            SupportPageLocators.TOPIC_DROPDOWN(id)
        ))
        return id
    
    def change_topic(self, topic):
        id = self.open_topic_dropdown()

        self.click(locator=SupportPageLocators.TOPIC_ITEM(id, topic))

        self.wait().until(EC.invisibility_of_element_located(SupportPageLocators.TOPIC_DROPDOWN(id)))

        new_id = self.open_topic_dropdown()

        assert self.wait().until(EC.visibility_of_element_located(
                SupportPageLocators.TOPIC_ITEM(new_id, topic)
        )).is_displayed()

    def enter_message(self, message):
        return self.update_input_field(
            message,
            locator=SupportPageLocators.MESSAGE_FORM,
        )
    
    def enter_name(self, name):
        return self.update_input_field(
            name,
            locator=SupportPageLocators.NAME_FORM,
        )
    
    def enter_email(self, email):
        return self.update_input_field(
            email,
            locator=SupportPageLocators.EMAIL_FORM,
        )

    def get_error(self, locator: Locator = None) -> WebElement:
        return self.find(
            SupportPageLocators.ERROR_MESSAGE,
            locator_to_find_in=locator,
        )
