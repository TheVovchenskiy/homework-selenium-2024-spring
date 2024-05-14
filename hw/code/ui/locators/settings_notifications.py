from selenium.webdriver.common.by import By


class SettingsNotificationsPageLocators:
    TAB_ITEM = (By.XPATH, '//*[@data-testid="tabs-item-settings.notifications"]')

    EMAIL_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@aria-label, "@")]')
    EMAIL_CHECKBOX_BUTTON = (By.XPATH, EMAIL_CHECKBOX[1] + '/../../..')

    NOTIFICATIONS_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@aria-label, "Уведомления ВКонтакте")]')
    NOTIFICATIONS_CHECKBOX_BUTTON = (By.XPATH, NOTIFICATIONS_CHECKBOX[1] + '/../../..')

    TELEGRAM_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@aria-label, "Сообщение в Telegram")]')
    TELEGRAM_CHECKBOX_BUTTON = (By.XPATH, TELEGRAM_CHECKBOX[1] + '/../../..')
    # TELEGRAM_BUTTON = (By.XPATH, '//button[span[span[contains(text(), "Сообщение в Telegram")]]]')

    WARNING = (By.CLASS_NAME, 'Warning_warning__xKzW3')

    DISABLED_CHECKBOXES = (By.XPATH, '//label[input[@type="checkbox" and @disabled]]')
