from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


import allure


class LoginPage(BasePage):
    @allure.step('Login')
    def login(self):
        if self.is_opened(url='https://ads.vk.com/hq/overview', timeout=120):
            return MainPage(self.driver)

