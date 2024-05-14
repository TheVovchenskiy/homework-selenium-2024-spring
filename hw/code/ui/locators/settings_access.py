from selenium.webdriver.common.by import By


class SettingsAccessPageLocators:
    TAB_ITEM = (By.XPATH, '//*[@data-testid="tabs-item-settings.access"]')

    MORE_BUTTON = (By.XPATH, '//*[@href="/help/articles/additionalaccounts"]')

    ADD_CABINET_BUTTON = (By.XPATH, '//*[@data-testid="add-user"]')
