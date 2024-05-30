from selenium.webdriver.support import expected_conditions as EC
from base import BaseCase
from ui.locators.surveys_locators import SurveysPageLocators
from ui.pages import surveys_page

from ui.fixtures import *

MAX_LENGTH_EXCEEDED = "Превышена максимальная длина поля"
REQUIRED_FILED = "Обязательное поле"
QUESTION_FOOTER_ERROR = "Вопрос должен быть не пустым и содержать минимум 2 ответа"
AT_LEAST_1_OPTION_MUST_BE_SELECTED = "Выберите хотя бы 1 вариант ответа"
HTTPS_REQUIRED = "Необходимо указать протокол http(s)"
INVALID_URL = "Невалидный url"

class TestSurveysCase(BaseCase):
    def surveys_setup(self):
        self.surveys_page = surveys_page.SurveysPage(self.driver)

    @pytest.fixture
    def open_survey_creation_modal_window(self):
        self.surveys_page.press_create_survey_button()

    @pytest.mark.skip('skip')
    def test_survey_name_input(self, open_survey_creation_modal_window):
        for input, expected_error in [
            ("", REQUIRED_FILED),
            ("   ", REQUIRED_FILED),
            ("1"*256, MAX_LENGTH_EXCEEDED),
            ("Опрос-30-05-24", None)
        ]:
           self.surveys_page.enter_survey_name(input)
           self.surveys_page.press_questions_button()

           error_elem = self.surveys_page.get_error_elem_of_form("Название")
           if error_elem == None:
               assert expected_error == None
           else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_logo_uploading(self, open_survey_creation_modal_window):
        self.surveys_page.upload_logo()

    @pytest.mark.skip('skip')
    def test_close_modal_window_button(self, open_survey_creation_modal_window):
        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.SURVEY_MODAL_WINDOW)).is_displayed()

        self.surveys_page.press_close_modal_window_button()

        assert self.surveys_page.wait().until(EC.invisibility_of_element_located(SurveysPageLocators.SURVEY_MODAL_WINDOW))

    @pytest.mark.skip('skip')
    def test_company_name_input(self, open_survey_creation_modal_window):
        for input, expected_error in [
            ("", REQUIRED_FILED),
            ("   ", REQUIRED_FILED),
            ("1"*35, MAX_LENGTH_EXCEEDED),
            ("VK", None),
            (" "*35 + "VK", None)
        ]:
            self.surveys_page.enter_company_name(input)
            self.surveys_page.press_questions_button()

            error_elem = self.surveys_page.get_error_elem_of_form("Название компании")
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_survey_header_input(self, open_survey_creation_modal_window):
        for input, expected_error in [
            ("", REQUIRED_FILED),
            ("   ", REQUIRED_FILED),
            ("1"*55, MAX_LENGTH_EXCEEDED),
            ("Тестовый заголовок", None),
            (" "*55 + "Тестовый заголовок", None)
        ]:
            self.surveys_page.enter_survey_header(input)
            self.surveys_page.press_questions_button()

            error_elem = self.surveys_page.get_error_elem_of_form("Заголовок опроса")
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_survey_description_input(self, open_survey_creation_modal_window):
        for input, expected_error in [
            ("", REQUIRED_FILED),
            ("   ", REQUIRED_FILED),
            ("1"*355, MAX_LENGTH_EXCEEDED),
            ("Тестовое описание", None),
        ]:
            self.surveys_page.enter_survey_description(input)
            self.surveys_page.press_questions_button()

            error_elem = self.surveys_page.get_error_elem_of_form("Описание опроса")
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_first_step_correct_input(self, open_survey_creation_modal_window):
        self.surveys_page.enter_survey_name("Опрос-30-05-24")
        self.surveys_page.upload_logo()
        self.surveys_page.enter_company_name("VK")
        self.surveys_page.enter_survey_header("Тестовый заголовок")
        self.surveys_page.enter_survey_description("Тестовое описание")

        for header in ["Название", "Логотип", "Название компании", "Заголовок опроса", "Описание опроса"]:
            error_elem = self.surveys_page.get_error_elem_of_form(header)
            assert error_elem == None

        self.surveys_page.press_questions_button()

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.QUESTION_ITEM)).is_displayed()

    @pytest.fixture
    def open_second_step_modal_window(self):
        self.surveys_page.press_create_survey_button()

        self.surveys_page.enter_survey_name("Опрос-30-05-24")
        self.surveys_page.upload_logo()
        self.surveys_page.enter_company_name("VK")
        self.surveys_page.enter_survey_header("Тестовый заголовок")
        self.surveys_page.enter_survey_description("Тестовое описание")

        self.surveys_page.press_questions_button()

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.QUESTION_ITEM)).is_displayed()

    @pytest.mark.skip('skip')
    def test_back_button_from_second_step(self, open_second_step_modal_window):
        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.QUESTION_ITEM)).is_displayed()

        self.surveys_page.press_back_button()

        assert self.surveys_page.wait().until(EC.invisibility_of_element_located(SurveysPageLocators.QUESTION_ITEM))
        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.SURVEY_NAME_INPUT)).is_displayed()

    @pytest.mark.skip('skip')
    def test_question_type_button(self, open_second_step_modal_window):
        for option, name in [(SurveysPageLocators.ONE_OF_LIST, "Один из списка"), (SurveysPageLocators.SEVERAL_OF_LIST, "Несколько из списка"), 
                       (SurveysPageLocators.FREE_FORM_ANSWER, "Ответ в свободной форме"), (SurveysPageLocators.SCALE, "Шкала")]:
            
            self.surveys_page.select_option_from_question_type_dropdown(option)
            elem = self.surveys_page.find(locator=SurveysPageLocators.QUESTION_TYPE_BUTTON)
            assert elem.text == name

    @pytest.mark.skip('skip')
    def test_question_text_input(self, open_second_step_modal_window):
        question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        for input, expected_error in [
            ("", QUESTION_FOOTER_ERROR),
            ("   ", QUESTION_FOOTER_ERROR),
            ("1"*80, QUESTION_FOOTER_ERROR),
        ]:
            self.surveys_page.enter_question_text(input)
            self.surveys_page.press_result_button()

            error_elem = self.surveys_page.get_question_error_footer(question)
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

            assert len(self.surveys_page.find(SurveysPageLocators.QUESTION_INPUT).text) <= 68

    @pytest.mark.skip('skip')
    def test_question_answer_input(self, open_second_step_modal_window):
        question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)
        self.surveys_page.enter_question_text("Тестовый вопрос")

        for input1, input2, expected_error in [
            ("", "", QUESTION_FOOTER_ERROR),
            ("   ", "", QUESTION_FOOTER_ERROR),
            ("", "  ", QUESTION_FOOTER_ERROR),
            ("  ", "   ", QUESTION_FOOTER_ERROR),
            ("Вариант 1", "Вариант 2", None)
        ]:
            self.surveys_page.enter_answers_to_question(question, [input1, input2])
            self.surveys_page.press_result_button()

            error_elem = self.surveys_page.get_question_error_footer(question)
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_add_answer_button(self, open_second_step_modal_window):
        question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        for i in range (1, 5):
            self.surveys_page.press_add_answer_button(question)
            assert len(self.surveys_page.find_all(SurveysPageLocators.ANSWER_INPUT)) == i + 2
            assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.ADD_ANSWER)).is_displayed()

        self.surveys_page.press_add_answer_button(question)
        assert self.surveys_page.wait().until(EC.invisibility_of_element_located(SurveysPageLocators.ADD_ANSWER))

    @pytest.mark.skip('skip')
    def test_template_answers(self, open_second_step_modal_window):
        question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        assert self.surveys_page.get_template_answer_value(question) == None

        for option, value in [
            (SurveysPageLocators.ANOTHER_ANSWER, "Другое (свой ответ)"),
            (SurveysPageLocators.NONE_OF_THE_ABOVE, "Ничего из перечисленного"),
            (SurveysPageLocators.NOT_SURE, "Затрудняюсь ответить"),
            (SurveysPageLocators.YOUR_OWN_ANSWER, "Свой вариант")
        ]:
            self.surveys_page.select_template_answer(question, option)

            assert self.surveys_page.wait().until(EC.invisibility_of_element_located(SurveysPageLocators.TEMPLATE_ANSWER))
            assert self.surveys_page.get_template_answer_value(question) == value

            new_answer = self.surveys_page.get_answer_to_question_by_text(question, value)
            self.surveys_page.remove_answer(new_answer)

            assert self.surveys_page.wait().until(EC.invisibility_of_element(new_answer))

    @pytest.mark.skip('skip')
    def test_duplicate_button(self, open_second_step_modal_window):
        original_question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        self.surveys_page.enter_question_text("Тестовый вопрос")
        self.surveys_page.enter_answers_to_question(original_question, ["Вариант 1", "Вариант 2"])
        self.surveys_page.select_template_answer(original_question, SurveysPageLocators.NOT_SURE)

        self.surveys_page.press_duplicate_button(original_question)

        questions = self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)
        
        answers1 = self.surveys_page.get_answers_list(questions[0])
        answers2 = self.surveys_page.get_answers_list(questions[1])

        assert (answers1 != None) and (answers2 != None)

        for a1, a2 in zip(answers1, answers2):
            assert a1.get_attribute('value') == a2.get_attribute('value')

        assert self.surveys_page.get_question_text(questions[0]) == self.surveys_page.get_question_text(questions[1])
        assert self.surveys_page.get_template_answer_value(questions[0]) == self.surveys_page.get_template_answer_value(questions[1])

    @pytest.mark.skip('skip')
    def test_add_diaplay_condition_button(self, open_second_step_modal_window):
        original_question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        self.surveys_page.enter_question_text("Тестовый вопрос")
        self.surveys_page.enter_answers_to_question(original_question, ["Вариант 1", "Вариант 2"])

        self.surveys_page.press_duplicate_button(original_question)

        question2 = self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)[1]

        self.surveys_page.press_add_display_condition_button(question2)
        self.surveys_page.press_result_button()

        error_elem = self.surveys_page.get_error_elem_of_form("содержит любой из")
        assert error_elem.text == AT_LEAST_1_OPTION_MUST_BE_SELECTED

        self.surveys_page.select_conditional_answer(question2, "Вариант 2")
        self.surveys_page.press_result_button()

        assert self.surveys_page.wait().until(EC.invisibility_of_element(error_elem))

    @pytest.mark.skip('skip')
    def test_add_question_button(self, open_second_step_modal_window):
        assert len(self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)) == 1

        self.surveys_page.press_add_question_button()
        questions = self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)
        assert len(questions) == 2

        self.surveys_page.press_remove_question_button(questions[1])
        assert self.surveys_page.wait().until(EC.invisibility_of_element(questions[1]))

    @pytest.mark.skip('skip')
    def test_add_question_button(self, open_second_step_modal_window):
        assert len(self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)) == 1

        for i in range(1, 23):
            self.surveys_page.press_add_question_button()

            assert len(self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)) == i + 1
            assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.ADD_QUESTION_BUTTON)).is_displayed()
        
        self.surveys_page.press_add_question_button()
        assert len(self.surveys_page.find_all(SurveysPageLocators.QUESTION_ITEM)) == 24
        assert self.surveys_page.wait().until(EC.invisibility_of_element_located(SurveysPageLocators.ADD_QUESTION_BUTTON))

    @pytest.fixture
    def open_third_step_modal_window(self):
        self.surveys_page.press_create_survey_button()

        self.surveys_page.enter_survey_name("Опрос-30-05-24")
        self.surveys_page.upload_logo()
        self.surveys_page.enter_company_name("VK")
        self.surveys_page.enter_survey_header("Тестовый заголовок")
        self.surveys_page.enter_survey_description("Тестовое описание")

        self.surveys_page.press_questions_button()

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.QUESTION_ITEM)).is_displayed()

        question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        self.surveys_page.enter_question_text("Тестовый вопрос")
        self.surveys_page.enter_answers_to_question(question, ["Вариант 1", "Вариант 2"])

        self.surveys_page.press_result_button()

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.RESULT_HEADER_INPUT)).is_displayed()

    @pytest.mark.skip('skip')
    def test_header_input(self, open_third_step_modal_window):
        for input, expected_error in [
            ("", REQUIRED_FILED),
            ("   ", REQUIRED_FILED),
            ("1"*30, MAX_LENGTH_EXCEEDED),
            ("Спасибо!", None)
        ]:
            self.surveys_page.enter_result_header(input)
            self.surveys_page.press_run_survey_button()

            error_elem = self.surveys_page.get_error_elem_of_form("Заголовок")
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_description_input(self, open_third_step_modal_window):
        for input, expected_error in [
            ("", REQUIRED_FILED),
            ("1"*170, MAX_LENGTH_EXCEEDED),
            ("Подписывайтесь на нашу группу в VK!", None)
        ]:
            self.surveys_page.enter_result_description(input)
            self.surveys_page.press_run_survey_button()

            error_elem = self.surveys_page.get_error_elem_of_form("Описание")
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    @pytest.mark.skip('skip')
    def test_link_input(self, open_third_step_modal_window):
        self.surveys_page.enter_result_header("")

        self.surveys_page.press_add_link_button()
        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.LINK_INPUT)).is_displayed()

        for input, expected_error in [
            ("", None),
            ("    ", HTTPS_REQUIRED),
            ("ws://", HTTPS_REQUIRED),
            ("vk.com", HTTPS_REQUIRED),
            ("https://@", INVALID_URL),
            ("https://?", INVALID_URL),
            ("https:///", INVALID_URL),
            ("https://:", INVALID_URL),
            ("https://#", INVALID_URL),
            ("https://vk.com", None)
        ]:
            self.surveys_page.enter_result_link(input)
            self.surveys_page.press_run_survey_button()

            error_elem = self.surveys_page.get_error_elem_of_link_form()
            if error_elem == None:
               assert expected_error == None
            else:
               assert error_elem.text == expected_error

    def test_success_survey_creation(self):
        self.surveys_page.press_create_survey_button()

        self.surveys_page.enter_survey_name("Опрос-31-05-24")
        self.surveys_page.upload_logo()
        self.surveys_page.enter_company_name("VK")
        self.surveys_page.enter_survey_header("Тестовый заголовок")
        self.surveys_page.enter_survey_description("Тестовое описание")

        for header in ["Название", "Логотип", "Название компании", "Заголовок опроса", "Описание опроса"]:
            error_elem = self.surveys_page.get_error_elem_of_form(header)
            assert error_elem == None

        self.surveys_page.press_questions_button()

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.QUESTION_ITEM)).is_displayed()

        question = self.surveys_page.find(SurveysPageLocators.QUESTION_ITEM)

        self.surveys_page.enter_question_text("Тестовый вопрос")
        self.surveys_page.enter_answers_to_question(question, ["Вариант 1", "Вариант 2"])

        self.surveys_page.press_result_button()

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.RESULT_HEADER_INPUT)).is_displayed()

        self.surveys_page.enter_result_header("Спасибо за участие!")
        self.surveys_page.enter_result_description("Переходите по ссылке, чтобы познакомиться с нами")
        self.surveys_page.press_add_link_button()
        self.surveys_page.enter_result_link("https://vk.com/blablagroup")

        self.surveys_page.press_run_survey_button()

        assert self.surveys_page.wait().until(EC.invisibility_of_element_located(SurveysPageLocators.SURVEY_MODAL_WINDOW))

        assert self.surveys_page.wait().until(EC.visibility_of_element_located(SurveysPageLocators.SURVEY_RECORD("Опрос-31-05-24"))).is_displayed()

