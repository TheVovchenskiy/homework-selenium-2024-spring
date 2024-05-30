from selenium.webdriver.common.by import By

from ui.locators.base_locators import Locator, locator_xpath_parent


class SettingsPageLocators:
    SETTINGS_BUTTON = (By.XPATH, '//*[@data-route="settings"]')

    SETTINGS_CONTAINER = (By.ID, 'settings')

    PHONE_INPUT = (By.XPATH, '//*[@data-testid="general-phone"]')
    PHONE_BLOCK = locator_xpath_parent(PHONE_INPUT, 2)

    EMAIL_INPUT = (By.XPATH, '//*[@data-testid="general-email"]')
    ADD_EMAIL_BUTTON = (By.XPATH, '//*[@data-testid="add-email"]')

    @staticmethod
    def ADDITIONAL_EMAIL_INPUT(id: int) -> Locator:
        return (By.XPATH, f'//*[@data-testid="email-{id}"]')
    
    @staticmethod
    def ADDITIONAL_EMAIL_BLOCK(id: int) -> Locator:
        return locator_xpath_parent(SettingsPageLocators.ADDITIONAL_EMAIL_INPUT(id), 5)

    REMOVE_EMAIL_BUTTON = (By.XPATH, '//*[@aria-label="Удалить"]')

    NAME_INPUT = (By.XPATH, '//*[@data-testid="general-ord-name"]')
    NAME_BLOCK = locator_xpath_parent(NAME_INPUT, 2)

    INN_INPUT = (By.XPATH, '//*[@data-testid="general-ord-inn"]')
    INN_BLOCK = locator_xpath_parent(INN_INPUT, 2)

    CABINET_INPUT = (By.XPATH, '//*[@data-testid="account-item"]')
    CABINET_BLOCK = locator_xpath_parent(CABINET_INPUT, 2)

    SAVE_BUTTON = (By.XPATH, '//*[@data-testid="settings-save"]')
    CANCEL_BUTTON = (By.XPATH, '//*[@data-testid="settings-cancel"]')

    LANGUAGE_CURR_LANG = (By.XPATH, '//span[contains(text(), "RU") or contains(text(), "EN")]')
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

    CONNECT_CABINET = (By.XPATH, '//div[div/div/span[contains(text(), "Привязать кабинет myTarget")]]')
    CONNECT_CABINET_MODAL = (By.XPATH, '//div[contains(@id, "_modal_")]')

    API_ACCESS_BUTTON = (By.CLASS_NAME, 'ApiAccess_wrapper__QEwLb')
    API_ACCESS_MODAL = (By.XPATH, '//div[contains(@id, "_modal_")]')

    API_ACCESS_NAME_BLOCK = (By.XPATH, '//*[@name="name"]')
    API_ACCESS_NAME_INPUT = (By.XPATH, './/input[@placeholder="Введите ФИО"]')

    API_ACCESS_PHONE_BLOCK = (By.XPATH, '//*[@name="phone"]')
    API_ACCESS_PHONE_INPUT = (By.XPATH, './/input[@placeholder="Введите номер телефона"]')

    API_ACCESS_EMAIL_BLOCK = (By.XPATH, '//*[@name="email"]')
    API_ACCESS_EMAIL_INPUT = (By.XPATH, './/input[@placeholder="Введите адрес электронной почты"]')

    API_ACCESS_SAVE_BUTTON = (By.XPATH, '//button[@type="submit" and @title="Запросить доступ"]')
    API_ACCESS_CANCEL_BUTTON = (By.XPATH, './/button[@type="button"]')

    LOGOUT_ALL_DEVICES_BUTTON = (By.XPATH, '//button[span/span[contains(text(), "Выйти из других устройств")]]')
    LOGOUT_ALL_DEVICES_MESSAGE = (By.XPATH, '//div[contains(text(), "Активные сеансы на других устройствах успешно завершены.")]')

    DELETE_CABINET_BUTTON = (By.XPATH, '//button[span/span[contains(text(), "Удалить кабинет")]]')
    DELETE_CABINET_MODAL = (By.XPATH, '//div[contains(text(), "Удалить кабинет ")]')

    ERROR_MESSAGE = (By.XPATH, './/span[@role="alert"]')

    WARNING = (By.XPATH, './/*[contains(@class, "Warning_container" and contains(@class, "VerificationInfo_warning"))]')
