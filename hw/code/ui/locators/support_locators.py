from selenium.webdriver.common.by import By

class SupportPageLocators:
    MODAL_WINDOW = (By.XPATH, '//div[contains(@id, "_modal_")]')
    SUCCESS_MODAL_WINDOW = (By.XPATH, '//div[contains(@class, "ModalManagerPage_modalContent")]')

    SUPPORT_BUTTON = (By.XPATH, '//span[contains(text(), "Помощь")]')
    ASK_QUESTION_BUTTON = (By.XPATH, '//span[contains(text(), "Задать вопрос")]')

    QUESTION_FORM = (By.CLASS_NAME, 'ModalManagerPage_modalContent__ybbav')

    FAQ_HREF = (By.XPATH, '//*[@href="https://ads.vk.com/help/articles/partner_faq"]')

    TOPIC_BUTTON = (By.XPATH, '//*[@role="combobox"]')

    MESSAGE_FORM = (By.XPATH, '//*[@name="message"]')
    NAME_FORM = (By.XPATH, '//*[@name="name"]')
    EMAIL_FORM = (By.XPATH, '//*[@name="email"]')

    ERROR_MESSAGE = (By.XPATH, './/span[@role="alert"]')

    CLOSE_BUTTON = (By.XPATH, '//*[@aria-label="Закрыть"]')

    CANCEL_BUTTON = (By.XPATH, '//*[@data-testid="cancel"]')
    SUMBIT_BUTTON = (By.XPATH, '//*[@data-testid="submit"]')

    @staticmethod
    def TOPIC_DROPDOWN(id: str):
        return (By.ID, id)
    
    @staticmethod
    def TOPIC_ITEM(id: str, topic: str):
        return (By.ID, f'{id}-{topic}')
    
    @staticmethod
    def ERROR_OF_FIELD(name: str):
        return (By.XPATH, f'.//h5[contains(text(), "{name}")]/../span[@role="alert"]')