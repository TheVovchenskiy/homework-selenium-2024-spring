import time
from ui.pages.base_page import DEFAULT_TIMEOUT
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators
from ui.pages.main_page import MainPage


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


ERR_REQUIRED_FIELD = 'Обязательное поле'
ERR_ONLY_SPACES = 'Значение не может содержать только пробелы'

ERR_INVALID_PHONE_NUMBER = 'Некорректный номер телефона'
ERR_INVALID_PHONE_LENGTH = 'Телефон не может быть короче 12 цифр'

ERR_INVALID_EMAIL = 'Некорректный email адрес'

ERR_INVALID_NAME_SYMBOLS = 'Некорректные символы. Разрешена только кириллица дефис и пробел'

ERR_INVALID_INN_LENGTH = 'Длина ИНН должна быть 12 символов'
ERR_INVALID_INN = 'Невалидный ИНН'
ERR_INCORRECT_INN = 'Некорректный ИНН'

DEFAULT_PHONE = '+71234567890'
DEFAULT_NAME = 'Иван'
DEFAULT_INN = '123456789012'
DEFAULT_CABINET = 'кабинет'


class SettingsPage(MainPage):
    url = 'https://ads.vk.com/hq/settings'

    def save_cancel_is_visible(self) -> bool:
        time.sleep(0.5)
        save_button = self.find(SettingsPageLocators.SAVE_BUTTON)
        cancel_button = self.find(
            SettingsPageLocators.CANCEL_BUTTON)
        return save_button.is_displayed() and cancel_button.is_displayed()

    def press_button(self, locator: Locator):
        time.sleep(0.5)
        self.click(locator, timeout=5)
        time.sleep(0.5)

    def press_save(self, expect_save=False):
        if self.save_cancel_is_visible():
            self.press_button(SettingsPageLocators.SAVE_BUTTON)
            if expect_save:
                if self.wait_until_true(lambda: not self.save_cancel_is_visible()):
                    return

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

    def update_name(self, new_name: str) -> tuple[str, str]:
        return self.update_input_field(
            SettingsPageLocators.NAME_INPUT,
            new_name,
        )

    def update_inn(self, new_inn: str) -> tuple[str, str]:
        return self.update_input_field(
            SettingsPageLocators.INN_INPUT,
            new_inn,
        )

    def update_cabinet(self, new_cabinet: str) -> tuple[str, str]:
        return self.update_input_field(
            SettingsPageLocators.CABINET_INPUT,
            new_cabinet,
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

    def open_language_dropdown(self):
        elem = self.find(SettingsPageLocators.LANGUAGE_BUTTON)

        id = elem.get_attribute('aria-owns')
        print(id)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
        # self.click(SettingsPageLocators.LANGUAGE_BUTTON)
        self.wait().until(EC.visibility_of_element_located(
            SettingsPageLocators.LANGUAGE_DROPDOWN(id)
        ))
        return id

    def get_curr_language(self) -> str:
        elem = self.find(SettingsPageLocators.LANGUAGE_CURR_LANG)

        return elem.text

    def assert_chosen_language(self, lang_elem: WebElement):
        assert lang_elem.get_attribute('aria-selected') == 'true'

    def change_language(self):
        target_elem = self.find(SettingsPageLocators.LANGUAGE_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            target_elem,
        )

        curr_language = self.get_curr_language()

        id = self.open_language_dropdown()

        if curr_language == 'RU':
            ru_elem = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_RU(id)
            ))
            self.assert_chosen_language(ru_elem)

            self.click(SettingsPageLocators.LANGUAGE_EN(id))
            time.sleep(1)

            id = self.open_language_dropdown()

            en_elem = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_EN(id)
            ))
            self.assert_chosen_language(en_elem)
        elif curr_language == 'EN':
            en_elem = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_EN(id)
            ))
            self.assert_chosen_language(en_elem)

            self.click(SettingsPageLocators.LANGUAGE_RU(id))

            id = self.open_language_dropdown()

            ru_elem = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_RU(id)
            ))
            self.assert_chosen_language(ru_elem)

        self.click(SettingsPageLocators.LANGUAGE_BUTTON)
