from ui.pages.base_page import BasePage
from ui.locators.settings_locators import SettingsPageLocators


class MainPage(BasePage):
    url = 'https://ads.vk.com/hq/overview'

    def go_to_settings(self):
        self.click(SettingsPageLocators.SETTINGS_BUTTON_LOCATOR, 5)
