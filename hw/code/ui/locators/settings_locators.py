from selenium.webdriver.common.by import By

from ui.locators.base_locators import Locator


class SettingsPageLocators:
    SETTINGS_BUTTON = (By.XPATH, '//*[@data-route="settings"]')

    SETTINGS_CONTAINER = (By.ID, 'settings')
    
    PHONE_BLOCK = (By.XPATH, '//*[@id="settings"]/div/form/section[2]/div[2]/div[1]')
    PHONE_INPUT = (By.XPATH, '//*[@data-testid="general-phone"]')

    EMAIL_INPUT = (By.XPATH, '//*[@data-testid="general-email"]')
    ADD_EMAIL_BUTTON = (By.XPATH, '//*[@data-testid="add-email"]')
    ADDITIONAL_EMAIL_BLOCK = (By.XPATH, '//*[@class="vkuiFormItem__removable vkuiInternalFormItem__removable"]')

    @staticmethod
    def ADDITIONAL_EMAIL_INPUT(id: int) -> Locator:
        return (By.XPATH, f'//*[@data-testid="email-{id}"]')
    REMOVE_EMAIL_BUTTON = (By.XPATH, '//*[@aria-label="Удалить"]')

    NAME_BLOCK = (By.XPATH, '//*[@id="settings"]/div/form/section[3]/div[2]/div[1]')
    NAME_INPUT = (By.XPATH, '//*[@data-testid="general-ord-name"]')

    INN_BLOCK = (By.XPATH, '//*[@id="settings"]/div/form/section[3]/div[2]/div[2]')
    INN_INPUT = (By.XPATH, '//*[@data-testid="general-ord-inn"]')

    CABINET_BLOCK = (By.XPATH, '//*[@id="settings"]/div/form/section[4]/div[2]/div[1]')
    CABINET_INPUT = (By.XPATH, '//*[@data-testid="account-item"]')

    SAVE_BUTTON = (By.XPATH, '//*[@data-testid="settings-save"]')
    CANCEL_BUTTON = (By.XPATH, '//*[@data-testid="settings-cancel"]')

    LANGUAGE_CURR_LANG = (By.XPATH, '//*[@id="settings"]/div/form/section[4]/div[2]/div[2]/div/div/div/div/div/span')
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

    ERROR_MESSAGE = (By.XPATH, '//span[@role="alert"]')

    WARNING = (By.XPATH, '//*[@class="Warning_container__WlR61 VerificationInfo_warning__Fwwj+"]')
