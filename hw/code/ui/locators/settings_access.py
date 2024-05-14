from selenium.webdriver.common.by import By


class SettingsAccessPageLocators:
    TAB_ITEM = (By.XPATH, '//*[@data-testid="tabs-item-settings.access"]')

    MORE_BUTTON = (By.XPATH, '//*[@href="/help/articles/additionalaccounts"]')

    ADD_CABINET_BUTTON = (By.XPATH, '//*[@data-testid="add-user"]')

    ADD_CABINET_MODAL = (By.XPATH, '//div[@aria-modal="true"]')

    ACCOUNT_ID_INPUT = (By.XPATH, '//*[@data-testid="userid-input"]')
    ACCOUNT_ID_BLOCK = (By.XPATH, ACCOUNT_ID_INPUT[1] + '/../..')

    READONLY_ACCESS_INPUT = (By.XPATH, '//input[@name="access" and @value="vkads_full_readonly_access"]')
    READONLY_ACCESS_RADIOBUTTON = (By.XPATH, READONLY_ACCESS_INPUT[1] + '/..')

    FULL_ACCESS_INPUT = (By.XPATH, '//input[@name="access" and @value="full_access"]')
    FULL_ACCESS_RADIOBUTTON = (By.XPATH, FULL_ACCESS_INPUT[1] + '/..')

    CHECKBOX = (By.XPATH, '//input[@type="checkbox"]')
    CHECKBOX_BUTTON = (By.XPATH, CHECKBOX[1] + '/..')

    SAVE_BUTTON = (By.XPATH, '//*[@data-testid="submit"]')
