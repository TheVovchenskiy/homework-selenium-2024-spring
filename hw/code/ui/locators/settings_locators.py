from selenium.webdriver.common.by import By

from ui.locators.base_locators import Locator


class SettingsPageLocators:
    SETTINGS_BUTTON = (By.XPATH, '//*[@data-route="settings"]')

    SETTINGS_CONTAINER = (By.ID, 'settings')

    PHONE_BLOCK = (
        By.XPATH, '//*[@id="settings"]/div/form/section[2]/div[2]/div[1]')
    PHONE_INPUT = (By.XPATH, '//*[@data-testid="general-phone"]')

    EMAIL_INPUT = (By.XPATH, '//*[@data-testid="general-email"]')
    ADD_EMAIL_BUTTON = (By.XPATH, '//*[@data-testid="add-email"]')
    ADDITIONAL_EMAIL_BLOCK = (
        By.XPATH, '//*[@class="vkuiFormItem__removable vkuiInternalFormItem__removable"]')

    @staticmethod
    def ADDITIONAL_EMAIL_INPUT(id: int) -> Locator:
        return (By.XPATH, f'//*[@data-testid="email-{id}"]')
    REMOVE_EMAIL_BUTTON = (By.XPATH, '//*[@aria-label="Удалить"]')

    NAME_BLOCK = (
        By.XPATH, '//*[@id="settings"]/div/form/section[3]/div[2]/div[1]')
    NAME_INPUT = (By.XPATH, '//*[@data-testid="general-ord-name"]')

    INN_BLOCK = (
        By.XPATH, '//*[@id="settings"]/div/form/section[3]/div[2]/div[2]')
    INN_INPUT = (By.XPATH, '//*[@data-testid="general-ord-inn"]')

    CABINET_BLOCK = (
        By.XPATH, '//*[@id="settings"]/div/form/section[4]/div[2]/div[1]')
    CABINET_INPUT = (By.XPATH, '//*[@data-testid="account-item"]')

    SAVE_BUTTON = (By.XPATH, '//*[@data-testid="settings-save"]')
    CANCEL_BUTTON = (By.XPATH, '//*[@data-testid="settings-cancel"]')

    LANGUAGE_CURR_LANG = (
        By.XPATH, '//*[@id="settings"]/div/form/section[4]/div[2]/div[2]/div/div/div/div/div/span')
    LANGUAGE_BUTTON = (By.XPATH, '//*[@data-testid="interface-language"]')

    @staticmethod
    def LANGUAGE_DROPDOWN(id: str):
        return (By.ID, id)

    @staticmethod
    def LANGUAGE_RU(id: str):
        return (By.ID, f'{id}-ru')

    @staticmethod
    def LANGUAGE_EN(id: str):
        return (By.ID, f'{id}-en')

    CONNECT_CABINET = (By.XPATH, '//*[@id="settings"]/div/form/section[5]/div[2]')
    CONNECT_CABINET_MODAL = (By.ID, '_modal_33')

    API_ACCESS_BUTTON = (By.CLASS_NAME, 'ApiAccess_wrapper__QEwLb')
    API_ACCESS_MODAL = (By.ID, '_modal_32')

    API_ACCESS_NAME_BLOCK = (By.XPATH, '//*[@name="name"]')
    API_ACCESS_NAME_INPUT = (By.XPATH, './/input[@placeholder="Введите ФИО"]')

    API_ACCESS_PHONE_BLOCK = (By.XPATH, '//*[@name="phone"]')
    API_ACCESS_PHONE_INPUT = (By.XPATH, './/input[@placeholder="Введите номер телефона"]')

    API_ACCESS_EMAIL_BLOCK = (By.XPATH, '//*[@name="email"]')
    API_ACCESS_EMAIL_INPUT = (By.XPATH, './/input[@placeholder="Введите адрес электронной почты"]')

    API_ACCESS_SAVE_BUTTON = (By.XPATH, '//button[@type="submit" and @title="Запросить доступ"]')
    API_ACCESS_CANCEL_BUTTON = (By.XPATH, './/button[@type="button"]')

    LOGOUT_ALL_DEVICES_BUTTON = (By.XPATH, '//button[span[span[contains(text(), "Выйти из других устройств")]]]')
    LOGOUT_ALL_DEVICES_MESSAGE = (By.XPATH, '//div[contains(text(), "Активные сеансы на других устройствах успешно завершены.")]')

    DELETE_CABINET_BUTTON = (By.XPATH, '//button[span[span[contains(text(), "Удалить кабинет")]]]')
    DELETE_CABINET_MODAL = (By.XPATH, '//div[contains(text(), "Удалить кабинет ")]')

    ERROR_MESSAGE = (By.XPATH, './/span[@role="alert"]')

    WARNING = (By.XPATH, './/*[@class="Warning_container__WlR61 VerificationInfo_warning__Fwwj+"]')
