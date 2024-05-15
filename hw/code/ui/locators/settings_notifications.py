from selenium.webdriver.common.by import By


from ui.locators.base_locators import locator_xpath_parent


class SettingsNotificationsPageLocators:
    TAB_ITEM = (By.XPATH, '//*[@data-testid="tabs-item-settings.notifications"]')

    EMAIL_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@aria-label, "@")]')
    EMAIL_CHECKBOX_BUTTON = locator_xpath_parent(EMAIL_CHECKBOX, 3)

    NOTIFICATIONS_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@aria-label, "Уведомления ВКонтакте")]')
    NOTIFICATIONS_CHECKBOX_BUTTON = locator_xpath_parent(NOTIFICATIONS_CHECKBOX, 3)

    TELEGRAM_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@aria-label, "Сообщение в Telegram")]')
    TELEGRAM_CHECKBOX_BUTTON = locator_xpath_parent(TELEGRAM_CHECKBOX, 3)

    WARNING = (By.CLASS_NAME, 'Warning_warning__xKzW3')

    DISABLED_CHECKBOXES = (By.XPATH, '//label[input[@type="checkbox" and @disabled]]')
