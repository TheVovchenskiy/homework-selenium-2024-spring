import os
from selenium.webdriver.common.by import By
from ui.pages.base_page import MAX_RETRIES_COUNT
from ui.locators.surveys_locators import SurveysPageLocators
from ui.pages.base_page import BasePage


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from retry import retry

class SurveysPage(BasePage):
    url = 'https://ads.vk.com/hq/leadads/surveys'

    @retry(MAX_RETRIES_COUNT)
    def press_create_survey_button(self):
        #elem = self.find(SurveysPageLocators.CREATE_SURVEY_BUTTON)
        elem = self.wait().until(EC.presence_of_element_located(SurveysPageLocators.CREATE_SURVEY_BUTTON))
        elem.click()
        #modal_window_elem = self.find(SurveysPageLocators.SURVEY_MODAL_WINDOW)
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.SURVEY_MODAL_WINDOW))

    def press_close_modal_window_button(self):
        elem = self.wait().until(EC.presence_of_element_located(SurveysPageLocators.CLOSE_MODAL_WINDOW_BUTTON))
        elem.click()
        modal_window_elem = self.find(SurveysPageLocators.SURVEY_MODAL_WINDOW)
        self.wait().until(EC.invisibility_of_element(modal_window_elem))

    def enter_survey_name(self, name):
        return self.update_input_field(
            name,
            locator=SurveysPageLocators.SURVEY_NAME_INPUT,
        )
    
    @retry(MAX_RETRIES_COUNT)
    def press_logo_button(self):
        elem = self.wait().until(EC.presence_of_element_located(SurveysPageLocators.UPLOAD_LOGO_BUTTON))
        elem.click()
        #modal_window_elem = self.find(SurveysPageLocators.UPLOAD_LOGO_MODAL_WINDOW)
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.UPLOAD_LOGO_MODAL_WINDOW))

    def upload_logo(self):
        self.press_logo_button()

        self.find(SurveysPageLocators.FILE_INPUT).send_keys(
            os.path.abspath(
                os.path.join('hw', 'files', 'imgs', 'right_img.png'),
            ),
        )

        assert len(self.find_all(SurveysPageLocators.LOGO_ITEM))

        self.click(elem=self.find_all(SurveysPageLocators.LOGO_ITEM)[0])

        assert self.wait_until_visible(SurveysPageLocators.LOGO_PREVIEW).is_displayed()
        assert self.wait_until_visible(SurveysPageLocators.LOGO_RIGHT_PREVIEW).is_displayed()

    def enter_company_name(self, name):
        return self.update_input_field(
            name,
            locator=SurveysPageLocators.SURVEY_COMPANY_NAME_INPUT,
        )
    
    def enter_survey_header(self, name):
        return self.update_input_field(
            name,
            locator=SurveysPageLocators.SURVEY_HEADER_INPUT,
        )
    
    def enter_survey_description(self, name):
        return self.update_input_field(
            name,
            locator=SurveysPageLocators.SURVEY_DESCRIPTION_INPUT,
        )

    def press_questions_button(self):
        elem = self.find(SurveysPageLocators.QUESTIONS_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_result_button(self):
        elem = self.find(SurveysPageLocators.RESULT_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
    
    def press_back_button(self):
        elem = self.find(SurveysPageLocators.BACK_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def show_question_type_dropdown(self):
        elem = self.find(SurveysPageLocators.QUESTION_TYPE_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.ONE_OF_LIST))

    def select_option_from_question_type_dropdown(self, option):
        self.show_question_type_dropdown()
        elem = self.find(option)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def enter_question_text(self, text):
        return self.update_input_field(
            text,
            locator=SurveysPageLocators.QUESTION_INPUT,
        )
    
    def enter_answers_to_question(self, question: WebElement, answers_list):
        answer_elems = question.find_elements(By.XPATH, './/input[@placeholder="Введите ответ"]')
        if len(answer_elems) == 0:
            return
        
        self.wait().until(EC.visibility_of(answer_elems[0]))
        for ans_elem, ans in zip(answer_elems, answers_list):
            self.update_input_field(input=ans_elem, new_input_data=ans)

    def press_add_answer_button(self, question: WebElement):
        button = question.find_element(By.XPATH, './/span[contains(text(), "Добавить вариант")]')
        self.wait().until(EC.element_to_be_clickable(button)).click()

    def select_template_answer(self, question: WebElement, option):
        button = question.find_element(By.XPATH, './/span[contains(text(), "Ответ из шаблона")]')
        self.wait().until(EC.element_to_be_clickable(button)).click()
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.ANOTHER_ANSWER))

        elem = self.find(option)
        self.wait().until(EC.element_to_be_clickable(elem)).click()

    def press_duplicate_button(self, question: WebElement):
        button = question.find_element(By.XPATH, './/button[contains(@class, "Question_duplicateQuestionButton")]')
        self.wait().until(EC.element_to_be_clickable(button)).click()

    def press_add_display_condition_button(self, question: WebElement):
        button = question.find_element(By.XPATH, './/button[contains(@class, "Question_conditionButton")]')
        self.wait().until(EC.element_to_be_clickable(button)).click()
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.ANSWER_CONDITION))

    def select_conditional_answer(self, parent_question: WebElement, text: str):
        form = parent_question.find_element(By.XPATH, './/input[@placeholder="Введите название" and contains(@id, "10_")]')
        self.wait().until(EC.element_to_be_clickable(form)).click()
        option = self.find(SurveysPageLocators.GET_ANSWER_ITEM(text))
        self.wait().until(EC.element_to_be_clickable(option)).click()

    def press_add_question_button(self):
        button = self.find(SurveysPageLocators.ADD_QUESTION_BUTTON)
        self.wait().until(EC.element_to_be_clickable(button)).click()

    def press_remove_question_button(self, question: WebElement):
        button = question.find_element(By.XPATH, '//button[contains(@class, "Question_removeQuestionButton")]')
        self.wait().until(EC.element_to_be_clickable(button)).click()

    def press_add_stop_screen_button(self):
        button = self.find(SurveysPageLocators.ADD_STOP_SCREEN)
        self.wait().until(EC.element_to_be_clickable(button)).click()
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.STOP_SCREEN))

    def select_stop_answer(self, text):
        stop_screen = self.find(SurveysPageLocators.STOP_SCREEN)
        stop_answer_form = stop_screen.find_element(By.XPATH, './/input[@aria-autocomplete="list" and contains(@id, "10_")]')
        self.wait().until(EC.element_to_be_clickable(stop_answer_form)).click()

        option = self.find(SurveysPageLocators.GET_STOP_ANSWER_ITEM(text))
        self.wait().until(EC.element_to_be_clickable(option)).click()

    def enter_stop_screen_header(self, text):
        return self.update_input_field(
            text,
            locator=SurveysPageLocators.STOP_SCREEN_HEADER,
        )

    def enter_stop_screen_description(self, text):
        return self.update_input_field(
            text,
            locator=SurveysPageLocators.STOP_SCREEN_DESCRIPTION,
        )
    
    def press_remove_stop_screen_button(self):
        elem = self.find(SurveysPageLocators.REMOVE_STOP_SCREEN_BUTTON)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
        stop_screen_elem = self.find(SurveysPageLocators.STOP_SCREEN)
        self.wait().until(EC.invisibility_of_element(stop_screen_elem))

    def enter_result_header(self, text):
        return self.update_input_field(
            text,
            locator=SurveysPageLocators.RESULT_HEADER_INPUT,
        )
    
    def enter_result_description(self, text):
        return self.update_input_field(
            text,
            locator=SurveysPageLocators.RESULT_DESCRIPTION_INPUT,
        )

    def press_add_link_button(self):
        elem = self.find(SurveysPageLocators.ADD_LINK)
        self.wait().until(EC.element_to_be_clickable(elem)).click()
        self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.LINK_INPUT))

    def enter_result_link(self, link):
        return self.update_input_field(
            link,
            locator=SurveysPageLocators.LINK_INPUT,
        )

    def press_run_survey_button(self):
        button = self.find(SurveysPageLocators.RUN_SURVEY_BUTTON)
        self.wait().until(EC.element_to_be_clickable(button)).click()

    def check_if_survey_created(self, name):
        return self.wait().until(EC.visibility_of_element_located(SurveysPageLocators.SURVEY_RECORD(name))).is_displayed()
    
    def get_error_elem_of_form(self, field_name) -> WebElement:
        parent_elem = self.find(SurveysPageLocators.GET_INPUT_PARENT_ELEM(field_name))
        try:
            error_elem = parent_elem.find_element(By.XPATH, './/span[@role="alert"]/div')
        except:
            return None
        
        return error_elem
    
    def get_error_elem_of_link_form(self) -> WebElement:
        parent_elem = self.find(SurveysPageLocators.GET_LINK_PARENT_ELEM())

        try:
            error_elem = parent_elem.find_element(By.XPATH, './/span[@role="alert"]/div')
        except:
            return None

        return error_elem
    
    def get_question_error_footer(self, question: WebElement) -> WebElement:
        try:
            error_footer = question.find_element(By.XPATH, './/span[contains(@class, "Question_errorText")]')
        except:
            return None
        
        return error_footer
    
    def get_question_items_by_question_text(self, text: str) -> WebElement:
        try:
            question_items = self.find_all(locator=SurveysPageLocators.QUESTION_ITEM)
        except:
            return None
        
        result = []
        for item in question_items:
            try:
                to_append = item.find_element(By.XPATH, f'.//textarea[text()="{text}"]')
            except:
                continue

            result.append(to_append)

        return result

    def get_template_answer_value(self, question: WebElement) -> str:
        try:
            elem = question.find_element(By.XPATH, './/input[@placeholder="Введите ответ" and @value and @disabled]')
        except:
            return None
        
        return elem.get_attribute('value')

    def remove_answer(self, answer: WebElement):
        try:
            remove_button = answer.find_element(By.XPATH, './/button[contains(@class, "Answer_removeBtn__")]')
        except:
            return
        
        self.wait().until(EC.element_to_be_clickable(remove_button)).click()
        self.wait().until(EC.invisibility_of_element(answer))

    def get_answer_to_question_by_text(self, question: WebElement, text: str) -> WebElement:
        try:
            answer = question.find_element(By.XPATH, f'.//input[@placeholder="Введите ответ" and @value="{text}"]/../..')
        except:
            return None
        
        return answer
    
    def get_answers_list(self, question: WebElement):
        try:
            list = question.find_elements(By.XPATH, './/input[@placeholder="Введите ответ" and @value]')
        except:
            return None
        
        return list
    
    def get_question_text(self, question: WebElement):
        try:
            text_field = question.find_element(By.XPATH, './/textarea[@placeholder="Текст вопроса"]')
        except:
            return None
        
        return text_field.text