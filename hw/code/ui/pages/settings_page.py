from ui.pages.base_page import DEFAULT_TIMEOUT, MAX_RETRIES_COUNT
from ui.locators.base_locators import Locator
from ui.locators.settings_locators import SettingsPageLocators
from ui.pages.main_page import MainPage
from retry import retry


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

ERR_API_INVALID_NAME = 'Некорректное имя'

ERR_API_INVALID_PHONE = 'Некорректный телефон'
ERR_API_INCORRECT_PHONE = 'Некорректный формат. Пример: +71234567890'

ERR_API_INVALID_EMAIL = 'Некорректный email'
ERR_API_INCORRECT_EMAIL = 'Некорректный формат. Пример: example@mail.ru'

DEFAULT_PHONE = '+71234567890'
DEFAULT_NAME = 'Иван'
DEFAULT_INN = '123456789012'
DEFAULT_CABINET = 'кабинет'


class SettingsPage(MainPage):
    url = 'https://ads.vk.com/hq/settings'

    def save_cancel_is_visible(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        return self.wait(timeout).until(EC.visibility_of_element_located(
            SettingsPageLocators.SAVE_BUTTON,
        )).is_displayed() and self.wait(timeout).until(EC.visibility_of_element_located(
            SettingsPageLocators.CANCEL_BUTTON,
        )).is_displayed()

    def save_cancel_is_invisible(self) -> bool:
        return not self.wait().until(EC.invisibility_of_element_located(
            SettingsPageLocators.SAVE_BUTTON,
        )).is_displayed() and not self.wait().until(EC.invisibility_of_element_located(
            SettingsPageLocators.CANCEL_BUTTON,
        )).is_displayed()

    def press_button(self, locator: Locator):
        self.click(
            elem=self.wait().until(EC.visibility_of_element_located(locator)),
        )

    @retry(tries=MAX_RETRIES_COUNT)
    def press_save(self, expect_save=False, timeout=DEFAULT_TIMEOUT):
        if self.save_cancel_is_visible(timeout):
            self.click(locator=SettingsPageLocators.SAVE_BUTTON,
                       timeout=timeout)
            if expect_save:
                if not self.wait(timeout).until(EC.invisibility_of_element(SettingsPageLocators.SAVE_BUTTON)).is_displayed():
                    return

    def press_cancel(self):
        if self.save_cancel_is_visible():
            self.press_button(SettingsPageLocators.CANCEL_BUTTON)

    def press_add_email(self):
        self.press_button(SettingsPageLocators.ADD_EMAIL_BUTTON)

    def get_error(self, locator: Locator = None, timeout: float = DEFAULT_TIMEOUT) -> WebElement:
        return self.find(
            SettingsPageLocators.ERROR_MESSAGE,
            locator_to_find_in=locator,
            timeout=timeout,
        )

    def get_phone_error(self, locator: Locator) -> WebElement:
        return self.get_error(SettingsPageLocators.PHONE_BLOCK)

    def update_phone_number(self, new_phone_number: str) -> tuple[str, str]:
        return self.update_input_field(
            new_phone_number,
            locator=SettingsPageLocators.PHONE_INPUT,
        )

    def update_name(self, new_name: str) -> tuple[str, str]:
        return self.update_input_field(
            new_name,
            locator=SettingsPageLocators.NAME_INPUT,
        )

    def update_inn(self, new_inn: str) -> tuple[str, str]:
        return self.update_input_field(
            new_inn,
            locator=SettingsPageLocators.INN_INPUT,
        )

    def update_cabinet(self, new_cabinet: str) -> tuple[str, str]:
        return self.update_input_field(
            new_cabinet,
            locator=SettingsPageLocators.CABINET_INPUT,
        )

    def update_email(self, id: int, email: str):
        return self.update_input_field(
            email,
            locator=SettingsPageLocators.ADDITIONAL_EMAIL_INPUT(id),
        )

    def has_warning(self, message: str) -> bool:
        elem = self.wait().until(EC.visibility_of(
            self.find(SettingsPageLocators.WARNING, timeout=5)))

        return message in elem.text

    def remove_additional_email(self):
        self.click(locator=SettingsPageLocators.REMOVE_EMAIL_BUTTON, timeout=5)

    def open_language_dropdown(self):
        elem = self.find(SettingsPageLocators.LANGUAGE_BUTTON)

        id = elem.get_attribute('aria-owns')
        self.click(elem=elem)
        if self.wait().until(EC.visibility_of_element_located(
            SettingsPageLocators.LANGUAGE_DROPDOWN(id)
        )).is_displayed():
            return id

    def get_curr_language(self) -> str:
        elem = self.wait().until(EC.visibility_of_element_located(SettingsPageLocators.LANGUAGE_CURR_LANG))

        return elem.text

    def assert_chosen_language(self, lang_elem: WebElement):
        assert lang_elem.get_attribute('aria-selected') == 'true'

    def scroll_to_connected_cabinet(self):
        self.scroll_to(SettingsPageLocators.CONNECT_CABINET)

    def change_language(self):
        self.scroll_to(SettingsPageLocators.LANGUAGE_BUTTON)

        curr_language = self.get_curr_language()

        id = self.open_language_dropdown()
        print(curr_language)

        if curr_language == 'RU':
            ru_elem_ru = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_RU(id)
            ))
            self.assert_chosen_language(ru_elem_ru)

            self.click(locator=SettingsPageLocators.LANGUAGE_EN(id))

            id = self.open_language_dropdown()

            ru_elem_en = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_EN(id)
            ))
            self.assert_chosen_language(ru_elem_en)
        elif curr_language == 'EN':
            en_elem_en = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_EN(id)
            ))
            self.assert_chosen_language(en_elem_en)

            self.click(locator=SettingsPageLocators.LANGUAGE_RU(id))

            id = self.open_language_dropdown()

            en_elem_ru = self.wait().until(EC.visibility_of_element_located(
                SettingsPageLocators.LANGUAGE_RU(id)
            ))
            self.assert_chosen_language(en_elem_ru)

        self.click(locator=SettingsPageLocators.LANGUAGE_BUTTON)
