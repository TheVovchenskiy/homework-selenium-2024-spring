import time
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators
from ui.pages.main_page import MainPage


from selenium.webdriver.remote.webelement import WebElement


ERR_REQUIRED_FIELD = 'Обязательное поле'

ERR_INVALID_PHONE_NUMBER = 'Некорректный номер телефона'
ERR_INVALID_PHONE_LENGTH = 'Телефон не может быть короче 12 цифр'

ERR_INVALID_EMAIL = 'Некорректный email адрес'

DEFAULT_PHONE = '+71234567890'
DEFAULT_NAME = 'Иван'
DEFAULT_INN = '123456789012'
DEFAULT_CABINET = 'кабинет'


class SettingsPage(MainPage):
    url = 'https://ads.vk.com/hq/settings'

    # def get_current_settings(self):
    #     phone = self.find(
    #         SettingsPageLocators.PHONE_INPUT
    #     ).get_attribute('value')
    #     name = self.find(
    #         SettingsPageLocators.NAME_INPUT
    #     ).get_attribute('value')
    #     inn = self.find(SettingsPageLocators.INN_INPUT).get_attribute('value')
    #     cabinet = self.find(
    #         SettingsPageLocators.CABINET_INPUT
    #     ).get_attribute('value')

    #     return {
    #         'phone': phone,
    #         'name': name,
    #         'inn': inn,
    #         'cabinet': cabinet,
    #     }

    # def set_settings(self, settings):
    #     if 'phone' in settings and settings['phone']:
    #         self.update_input_field(
    #             SettingsPageLocators.PHONE_INPUT,
    #             settings['phone'],
    #         )

    #     if 'name' in settings and settings['name']:
    #         self.update_input_field(
    #             SettingsPageLocators.NAME_INPUT,
    #             settings['name'],
    #         )

    #     if 'inn' in settings and settings['inn']:
    #         self.update_input_field(
    #             SettingsPageLocators.INN_INPUT,
    #             settings['inn'],
    #         )

    #     if 'cabinet' in settings and settings['cabinet']:
    #         self.update_input_field(
    #             SettingsPageLocators.CABINET_INPUT,
    #             settings['cabinet'],
    #         )

    #     self.press_save()

    def save_cancel_is_visible(self) -> bool:
        time.sleep(0.5)
        save_button = self.find(SettingsPageLocators.SAVE_BUTTON)
        cancel_button = self.find(
            SettingsPageLocators.CANCEL_BUTTON)
        return save_button.is_displayed() and cancel_button.is_displayed()

    def press_button(self, locator: Locator):
        time.sleep(0.5)
        self.click(locator, timeout=5)

    def press_save(self):
        if self.save_cancel_is_visible():
            self.press_button(SettingsPageLocators.SAVE_BUTTON)

    def press_cancel(self):
        if self.save_cancel_is_visible():
            self.press_button(SettingsPageLocators.CANCEL_BUTTON)

    def press_add_email(self):
        self.press_button(SettingsPageLocators.ADD_EMAIL_BUTTON)

    def get_error(self, locator: Locator = None) -> WebElement:
        return self.find(
            SettingsPageLocators.ERROR_MESSAGE,
            locator_to_find_in=locator,
        )

    def get_phone_error(self, locator: Locator) -> WebElement:
        return self.get_error(SettingsPageLocators.PHONE_BLOCK)

    def update_phone_number(self, new_phone_number: str) -> tuple[str, str]:
        return self.update_input_field(
            SettingsPageLocators.PHONE_INPUT,
            new_phone_number,
        )

    def update_email(self, id: int, email: str):
        return self.update_input_field(
            SettingsPageLocators.ADDITIONAL_EMAIL_INPUT(id),
            email,
        )

    def has_warning(self, message: str) -> bool:
        elem = self.find(SettingsPageLocators.WARNING, timeout=5)

        return message in elem.text

    def remove_additional_email(self):
        self.click(SettingsPageLocators.REMOVE_EMAIL_BUTTON, timeout=5)
