from selenium.webdriver.common.by import By


class SettingsPageLocators:
    SETTINGS_BUTTON = (By.XPATH, '//*[@data-route="settings"]')
    
    PHONE_BLOCK = (By.XPATH, '//*[@id="settings"]/div/form/section[2]/div[2]/div[1]')
    PHONE_INPUT = (By.XPATH, '//*[@data-testid="general-phone"]')

    EMAIL_INPUT = (By.XPATH, '//*[@data-testid="general-email"]')
    NAME_INPUT = (By.XPATH, '//*[@data-testid="general-ord-name"]')
    INN_INPUT = (By.XPATH, '//*[@data-testid="general-ord-inn"]')
    CABINET_INPUT = (By.XPATH, '//*[@data-testid="account-item"]')

    SAVE_BUTTON = (By.XPATH, '//*[@data-testid="settings-save"]')
    CANCEL_BUTTON = (By.XPATH, '//*[@data-testid="settings-cancel"]')

    ERROR_MESSAGE = (By.XPATH, '//span[@role="alert"]')

