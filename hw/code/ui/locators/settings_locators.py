from selenium.webdriver.common.by import By


class SettingsPageLocators:
    SETTINGS_BUTTON = (By.XPATH, '//*[@data-route="settings"]')
    PHONE_INPUT = (By.XPATH, '//*[@data-testid="general-phone"]')
    EMAIL_INPUT = (By.XPATH, '//*[@data-testid="general-email"]')
    NAME_INPUT = (By.XPATH, '//*[@data-testid="general-ord-name"]')
    INN_INPUT = (By.XPATH, '//*[@data-testid="general-ord-inn"]')
    CABINET_INPUT = (By.XPATH, '//*[@data-testid="account-item"]')
