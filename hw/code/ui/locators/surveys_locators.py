from selenium.webdriver.common.by import By

class SurveysPageLocators:
    CREATE_SURVEY_BUTTON = (By.XPATH, '//span[contains(text(), "Создать опрос")]')
    SURVEY_MODAL_WINDOW = (By.XPATH, '//div[contains(@class, "ModalSidebarPage_contentWithoutHeader")]')

    CLOSE_MODAL_WINDOW_BUTTON = (By.XPATH, '//button[@aria-label="close_button"]/..')
    QUESTIONS_BUTTON = (By.XPATH, '//span[contains(text(), "Вопросы")]')

    SURVEY_NAME_INPUT = (By.XPATH, '//input[@placeholder="Введите название"]')
    UPLOAD_LOGO_BUTTON = (By.XPATH, '//span[contains(text(), "Загрузить логотип")]')
    UPLOAD_LOGO_MODAL_WINDOW = (By.XPATH, '//div[contains(@class, "ModalSidebarPage_container__")]')
    SURVEY_COMPANY_NAME_INPUT = (By.XPATH, '//input[@placeholder="Введите название компании"]')
    SURVEY_HEADER_INPUT = (By.XPATH, '//input[@placeholder="Введите заголовок"]')
    SURVEY_DESCRIPTION_INPUT = (By.XPATH, '//textarea[@placeholder="Введите описание опроса"]')

    FILE_INPUT = (By.XPATH, '//input[@type="file" and @accept]')
    LOGO_ITEM = (By.XPATH, '//div[contains(@class, "ImageItems_imageItem")]')
    LOGO_PREVIEW = (By.XPATH, '//div[contains(@class, "Preview_activeLogoWrap__")]')
    LOGO_RIGHT_PREVIEW = (By.XPATH, '//img[@alt="Название компании"]')

    RESULT_BUTTON = (By.XPATH, '//span[contains(text(), "Результат")]')
    BACK_BUTTON = (By.XPATH, '//span[contains(text(), "Назад")]')

    QUESTION_TYPE_BUTTON = (By.XPATH, '//div[contains(@class, "HintSelector_hintSelectorButton")]')
    QUESTION_TYPE_DROPDOWN = (By.XPATH, '//div[contains(@class, "HintSelector_list")]')
    ONE_OF_LIST = (By.XPATH, '//span[contains(text(), "Один из списка")]')
    SEVERAL_OF_LIST = (By.XPATH, '//span[contains(text(), "Несколько из списка")]')
    FREE_FORM_ANSWER = (By.XPATH, '//span[contains(text(), "Ответ в свободной форме")]')
    SCALE = (By.XPATH, '//span[contains(text(), "Шкала")]')

    QUESTION_INPUT = (By.XPATH, '//textarea[@placeholder="Текст вопроса"]')
    ANSWER_INPUT = (By.XPATH, '//input[@placeholder="Введите ответ"]')

    ADD_ANSWER = (By.XPATH, '//span[contains(text(), "Добавить вариант")]')

    TEMPLATE_ANSWER = (By.XPATH, '//span[contains(text(), "Ответ из шаблона")]')
    ANOTHER_ANSWER = (By.XPATH, '//h5[contains(text(), "Другое (свой ответ)")]')
    NONE_OF_THE_ABOVE = (By.XPATH, '//h5[contains(text(), "Ничего из перечисленного")]')
    NOT_SURE = (By.XPATH, '//h5[contains(text(), "Затрудняюсь ответить")]')
    YOUR_OWN_ANSWER = (By.XPATH, '//h5[contains(text(), "Свой вариант")]')
    
    @staticmethod
    def GET_TEMPLATE_ANSWER_ITEM(text):
        return (By.XPATH, '//input[@placeholder="Введите ответ" and @value="Затрудняюсь ответить"]')

    DUPLICATE_BUTTON = (By.XPATH, '//button[contains(@class, "Question_duplicateQuestionButton")]')
    REMOVE_QUESTION_BUTTON = (By.XPATH, '//button[contains(@class, "Question_removeQuestionButton")]')
    
    ADD_DISPLAY_CONDITION_BUTTON = (By.XPATH, '//button[contains(@class, "Question_conditionButton")]')
    QUESTION_CONDITION = (By.XPATH, '//input[@aria-owns=":r19:"]')
    ANSWER_CONDITION = (By.XPATH, '//input[@placeholder="Введите название" and contains(@id, "10_")]')

    ADD_QUESTION_BUTTON = (By.XPATH, '//span[contains(text(), "Добавить вопрос")]')
    ADD_STOP_SCREEN = (By.XPATH, '//span[contains(text(), "Добавить стоп-экран")]')

    STOP_SCREEN = (By.XPATH, '//div[contains(@class, "StopScreen_stopScreen__")]')

    REMOVE_STOP_SCREEN_BUTTON = (By.XPATH, '//button[contains(@class, "StopScreen_removeButton")]')

    STOP_QUESTION_DROPDOWN = (By.XPATH, '//input[@aria-owns=":r5:"]')
    STOP_ANSWER_DROPDOWN = (By.XPATH, '//input[@aria-autocomplete="list" and contains(@id, "10_3")]')
    STOP_SCREEN_HEADER = (By.XPATH, '//input[@placeholder="Введите заголовок"]')
    STOP_SCREEN_DESCRIPTION = (By.XPATH, '//input[@placeholder="Введите описание опроса"]')

    RUN_SURVEY_BUTTON = (By.XPATH, '//span[contains(text(), "Запустить опрос")]')

    RESULT_HEADER_INPUT = (By.XPATH, '//input[@placeholder="Введите заголовок"]')
    RESULT_DESCRIPTION_INPUT = (By.XPATH, '//input[@placeholder="Введите описание: например, поблагодарите за прохождение опроса"]')

    ADD_LINK = (By.XPATH, '//span[contains(text(), "Добавить ссылку")]')
    LINK_INPUT = (By.XPATH, '//input[@placeholder="Введите ссылку"]')

    QUESTION_ITEM = (By.XPATH, '//div[contains(@class, "Question_question__")]')

    @staticmethod
    def QUESTION_CONDITION_DROPDOWN(id: str):
        return (By.ID, id)
    
    @staticmethod
    def ANSWER_CONDITION_DROPDOWN(id: str):
        return (By.ID, id)

    @staticmethod
    def GET_QUESTION_ITEM(id: str, name: str):
        return (By.ID, f'{id}-{name}')
    
    @staticmethod
    def GET_ANSWER_ITEM(name: str):
        return (By.XPATH, f'//div[contains(@class, "vkuiCustomSelectOption") and @title="{name}"]')

    @staticmethod
    def GET_STOP_QUESTION_ITEM(id: str, name: str):
        return (By.ID, f'{id}-{name}')
    
    @staticmethod
    def GET_STOP_ANSWER_ITEM(name: str):
        return (By.XPATH, f'//div[contains(@class, "vkuiCustomSelectOption") and @title="{name}"]')

    @staticmethod
    def SURVEY_RECORD(name: str):
        return (By.XPATH, f'//div[contains(@class, "ContextMenuWrapper_content") and contains(text(), "{name}")]')
    
    @staticmethod
    def GET_INPUT_PARENT_ELEM(name: str):
        return (By.XPATH, f'//h5[text()="{name}"]/..')
    
    def GET_LINK_PARENT_ELEM():
        return (By.XPATH, '//h2/span[text()="Ссылка"]/../..')