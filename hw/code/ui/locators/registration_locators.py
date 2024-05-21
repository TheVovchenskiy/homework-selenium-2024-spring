from selenium.webdriver.common.by import By

class RegistrationPageLocators:
    BACK_BUTTON = (By.XPATH, '//*[@data-testid="back-button"]')

    COUNTRY_BUTTON = (By.XPATH, '//*[@data-testid="country"]')
    CURRENCY_BUTTON = (By.XPATH, '//*[@data-testid="currency"]')

    EMAIL_INPUT = (By.XPATH, '//*[@data-testid="email"]')

    INDIVIDUAL_RADIO_BUTTON = (By.XPATH, '//*[@data-testid="physical"]')
    LEGAL_ENTITY_RADIO_BUTTON = (By.XPATH, '//span[contains(text(), "Юридическое лицо")]')
    LEGAL_ENTITY_INPUT = (By.XPATH, '//*[@data-testid="juridical"]')

    OFFER_CHECKBOX_TO_CLICK = (By.XPATH, '//div[contains(text(), "Создавая кабинет, вы принимаете условия")]')
    OFFER_CHECKBOX_TO_CHECK = (By.NAME, 'offer')

    ERROR_MESSAGE = (By.XPATH, './/span[@role="alert"]')
    BACKGROUND = (By.CLASS_NAME, 'vkuiPanel__centered')

    SIGN_UP_BUTTON = (By.XPATH, '//*[@data-testid="create-button"]')

    @staticmethod
    def COUNTRY_DROPDOWN(id: str):
        return (By.ID, id)
    
    @staticmethod
    def COUNTRY_ITEM(id: str, num: str):
        return (By.ID, f'{id}-{num}')
    
    @staticmethod
    def CURRENCY_DROPDOWN(id: str):
        return (By.ID, id)

    @staticmethod
    def CURRENCY_ITEM(id: str, name: str):
        return (By.ID, f'{id}-{name}')
    
    @staticmethod
    def ERROR_OF_FIELD(name: str):
        return (By.XPATH, f'.//h5[contains(text(), "{name}")]/../span[@role="alert"]')