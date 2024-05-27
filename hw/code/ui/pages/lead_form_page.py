import os
from typing import Any, Callable

import pytest
from ui.pages.base_page import DEFAULT_TIMEOUT, MAX_RETRIES_COUNT
from ui.locators.base_locators import Locator
from ui.locators.lead_form_locators import LeadFormLocators as locators
from ui.pages.main_page import MainPage
from retry import retry


from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


ERR_REQUIRED_FIELD = 'Обязательное поле'
ERR_MAX_FIELD_LEN = 'Превышена максимальная длина поля'
ERR_MAX_NEW_LINE_COUNT = 'Разрешено не более 2 переносов строк подряд'
ERR_VALUE_GT_ZERO = 'Значение должно быть больше нуля'
ERR_MAX_DISCOUNT_PERCENT = 'Запрещено указывать скидку более 100%'
ERR_INVALID_URL = 'Невалидный url'
ERR_INVALID_PHONE = 'Телефон должен начинаться с + и содержать только цифры'


TEST_LEAD_FORM_NAME = 'test lead form'
TEST_COMPANY_NAME = 'test company'
TEST_HEADER = 'test header'
TEST_DESCRIPTION = 'test description'


type TestCases = list[tuple[str, str | None, str | None]]


class LeadFormPage(MainPage):
    url = 'https://ads.vk.com/hq/leadads/leadforms'

    @retry(MAX_RETRIES_COUNT)
    def open_create_lead_form(self):
        if self.wait_until_visible(locators.CREATE_BUTTON).is_displayed():
            self.click(locator=locators.CREATE_BUTTON)
            self.wait_until_loaded([
                locators.MODAL,
                locators.SUBMIT_BUTTON,
                locators.CANCEL_BUTTON,
                locators.LID_FORM_NAME_INPUT,
            ])

    def get_error(self, locator: Locator = None, timeout: float = DEFAULT_TIMEOUT) -> WebElement:
        return self.find(
            locators.ERROR_MESSAGE,
            locator_to_find_in=locator,
            timeout=timeout,
        )

    @retry(exceptions=TimeoutException, tries=MAX_RETRIES_COUNT, delay=0.5)
    def expect_error(self, expected_error: str | None, block_locator: Locator) -> bool:
        if expected_error is None:
            try:
                existing_error = self.get_error(block_locator, 0.5)
            except TimeoutException:
                return True
            else:
                raise TimeoutException

        existing_error = self.get_error(block_locator, 1)
        if expected_error in existing_error.text:
            return True

        raise TimeoutException

    def submit_cancel_is_visible(self, timeout: float = DEFAULT_TIMEOUT) -> bool:
        return self.wait(timeout).until(EC.visibility_of_element_located(
            locators.SUBMIT_BUTTON,
        )).is_displayed() and self.wait(timeout).until(EC.visibility_of_element_located(
            locators.CANCEL_BUTTON,
        )).is_displayed()

    @retry(MAX_RETRIES_COUNT)
    def press_submit(self, expect_save=False, timeout=DEFAULT_TIMEOUT):
        if self.submit_cancel_is_visible(timeout):
            self.click(locator=locators.SUBMIT_BUTTON)
            if expect_save:
                if not self.wait(timeout).until(EC.invisibility_of_element(locators.SUBMIT_BUTTON)).is_displayed():
                    return

    def _check_input(
        self,
        block_locator: Locator,
        input_locator: Locator,
        test_cases: TestCases,
        *,
        preview_check: Callable[[str], bool] = None,
        save_after_test_case=True,
    ):
        prev_value = self.get_input_value(locator=input_locator)
        for new_value, expected_value, expected_error in test_cases:
            _, curr_value = self.update_input_field(
                new_value,
                locator=input_locator,
            )

            if expected_value:
                curr_value == expected_value

            if save_after_test_case:
                assert self.submit_cancel_is_visible()
                self.press_submit()

            assert self.expect_error(
                expected_error,
                block_locator,
            )

            if expected_error is None and preview_check:
                assert preview_check(curr_value)

        self.update_input_field(
            prev_value,
            locator=input_locator,
        )

    def check_lead_form_name_input(self, test_cases: TestCases):
        self._check_input(
            locators.LID_FORM_NAME_BLOCK,
            locators.LID_FORM_NAME_INPUT,
            test_cases,
        )

    def check_upload_logo(self):
        self.press_submit()

        assert self.expect_error(
            ERR_REQUIRED_FIELD,
            locators.ADD_LOGO_BLOCK,
        )

        self.click(locator=locators.ADD_LOGO_BUTTON)

        self.wait_until_visible(locators.MEDIA_HEADER)

        self.find(locators.FILE_INPUT).send_keys(
            os.path.abspath(
                os.path.join('hw', 'files', 'imgs', 'large_img.jpg'),
            ),
        )

        assert self.wait_until_visible(locators.FILE_ERROR_BANNER)\
            .is_displayed()

        self.find(locators.FILE_INPUT).send_keys(
            os.path.abspath(
                os.path.join('hw', 'files', 'imgs', 'right_img.png'),
            ),
        )

        assert len(self.find_all(locators.LOGO_ITEM))

        self.click(elem=self.find_all(locators.LOGO_ITEM)[0])

        assert self.wait_until_visible(locators.LOGO_PREVIEW).is_displayed()
        assert self.wait_until_visible(locators.LOGO_RIGHT_PREVIEW)\
            .is_displayed()

    def check_company_name_input(self, test_cases: TestCases):
        self._check_input(
            locators.COMPANY_NAME_BLOCK,
            locators.COMPANY_NAME_INPUT,
            test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('span', text)
            ).is_displayed()
        )

    def check_compact(
        self,
        header_test_cases: TestCases,
        description_test_cases: TestCases,
    ):
        self.click(locator=locators.COMPACT_LABEL)

        self._check_input(
            locators.HEADER_TEXT_BLOCK,
            locators.HEADER_TEXT_INPUT,
            header_test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('span', text)
            ).is_displayed()
        )
        self._check_input(
            locators.SHORT_DESCRIPTION_BLOCK,
            locators.SHORT_DESCRIPTION_INPUT,
            description_test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('span', text)
            ).is_displayed()
        )

    def check_long(
        self,
        header_test_cases: TestCases,
        description_test_cases: TestCases,
    ):

        self.click(locator=locators.LONG_TEXT_LABEL)

        self._check_input(
            locators.HEADER_TEXT_BLOCK,
            locators.HEADER_TEXT_INPUT,
            header_test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('h2', text)
            ).is_displayed()
        )
        self._check_input(
            locators.LONG_DESCRIPTION_BLOCK,
            locators.LONG_DESCRIPTION_INPUT,
            description_test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('div', text)
            ).is_displayed()
        )

    def check_award(
        self,
        discount_money_test_cases: TestCases,
        discount_percent_test_cases: TestCases,
        bonus_test_cases: TestCases,
    ):
        self.click(locator=locators.AWARD_LABEL)
        self._check_award_discount(
            discount_money_test_cases,
            discount_percent_test_cases,
        )

        self._check_award_bonus(bonus_test_cases)

    def _check_award_discount(
        self,
        money_test_cases: TestCases,
        percent_test_cases: TestCases,
    ):
        self.scroll_to(locators.DISCOUNT_RADIOBUTTON)
        discount_button = self.wait_until_visible(locators.DISCOUNT_BUTTON)
        self.click(elem=discount_button)
        assert self.find(locators.DISCOUNT_RADIOBUTTON).is_selected()

        self._check_award_discount_money(money_test_cases)
        self._check_award_discount_percent(percent_test_cases)

    def _check_award_discount_money(self, test_cases: TestCases):
        money_button = self.wait_until_visible(locators.MONEY_DISCOUNT_BUTTON)
        self.click(elem=money_button)
        assert self.find(locators.MONEY_DISCOUNT_INPUT)\
            .is_selected()

        self._check_input(
            locators.DISCOUNT_VALUE_BLOCK,
            locators.DISCOUNT_VALUE_INPUT,
            test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('div', f'{text} Р')
            ).is_displayed()
        )

    def _check_award_discount_percent(self, test_cases: TestCases):
        discount_button = self.wait_until_visible(
            locators.PERCENT_DISCOUNT_BUTTON)
        self.click(elem=discount_button)
        assert self.find(locators.PERCENT_DISCOUNT_INPUT)\
            .is_selected()

        self._check_input(
            locators.DISCOUNT_VALUE_BLOCK,
            locators.DISCOUNT_VALUE_INPUT,
            test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('div', f'{text} %')
            ).is_displayed()
        )

    def _check_award_bonus(
        self,
        test_cases: TestCases,
    ):
        bonus_button = self.wait_until_visible(locators.BONUS_BUTTON)
        self.click(elem=bonus_button)
        assert self.find(locators.BONUS_RADIOBUTTON)\
            .is_selected()

        self._check_input(
            locators.BONUS_VALUE_BLOCK,
            locators.BONUS_VALUE_INPUT,
            test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('h4', text)
            ).is_displayed()
        )

    def check_style(self):
        self.scroll_to(locators.STYLE_RED)
        red_style_button = self.wait_until_visible(locators.STYLE_RED)
        assert 'GradientSelector_roundActive' not in red_style_button\
            .get_attribute('class')

        self.click(elem=red_style_button)
        assert 'GradientSelector_roundActive' in red_style_button\
            .get_attribute('class')

    def complete_first_step(self):
        self.open_create_lead_form()

        self.update_input_field(
            TEST_LEAD_FORM_NAME,
            locator=locators.LID_FORM_NAME_INPUT,
        )

        self.check_upload_logo()

        self.update_input_field(
            TEST_COMPANY_NAME,
            locator=locators.COMPANY_NAME_INPUT,
        )

        self.update_input_field(
            TEST_HEADER,
            locator=locators.HEADER_TEXT_INPUT,
        )

        self.update_input_field(
            TEST_DESCRIPTION,
            locator=locators.SHORT_DESCRIPTION_INPUT,
        )

        self.press_submit()

        self.wait_until_loaded([
            locators.ADD_QUESTION_BUTTON,
            locators.ADD_CONTACT_INFO_BUTTON,
        ])

    def _check_add_questions(self):
        for i in range(1, 6):
            self.click(locator=locators.ADD_QUESTION_BUTTON)
            assert self.wait_until_visible(locators.QUESTIONS_CONTAINER(i))\
                .is_displayed()

        with pytest.raises(TimeoutException):
            self.find(locators.ADD_QUESTION_BUTTON, timeout=1)

        for i in range(5, 1, -1):
            self.click(locator=locators.REMOVE_QUESTION_BUTTON(i))

        self.wait_until_visible(locators.QUESTIONS_CONTAINER(1)).is_displayed()

    def check_question(self, question_test_cases: TestCases, answers_test_cases: TestCases):
        self._check_add_questions()

        self.scroll_to(locators.QUESTIONS_CONTAINER(1))

        with pytest.raises(TimeoutException):
            self.wait_until_visible(
                locators.QUESTIONS_ERROR_ICON(1), timeout=0.1)

        self.press_submit()

        assert self.wait_until_visible(
            locators.QUESTIONS_ERROR_ICON(1)).is_displayed()

        self.update_input_field('1', locator=locators.QUESTION_TEXT)
        for answer_input in self.find_all(locators.ANSWER_INPUT):
            self.update_input_field('1', input=answer_input)

        with pytest.raises(TimeoutException):
            self.wait_until_visible(
                locators.QUESTIONS_ERROR_ICON(1),
                timeout=0.1,
            )

        self._check_question_text(locators.QUESTION_TEXT, question_test_cases)

        self._check_question_answers(answers_test_cases)

        self.click(locator=locators.REMOVE_QUESTION_BUTTON(1))

    def _check_question_text(self, input_locator: Locator, test_cases: TestCases):
        prev_value = self.get_input_value(locator=input_locator)
        for new_value, expected_value, expected_error in test_cases:
            _, curr_value = self.update_input_field(
                new_value,
                locator=input_locator,
            )

            if expected_value:
                curr_value == expected_value

            if expected_error is None:
                with pytest.raises(TimeoutException):
                    self.wait_until_visible(
                        locators.QUESTIONS_ERROR_ICON(1),
                        timeout=0.1,
                    )
            else:
                assert self.wait_until_visible(locators.QUESTIONS_ERROR_ICON(1))\
                    .is_displayed()

        self.update_input_field(
            prev_value,
            locator=input_locator,
        )

    def _check_question_answers(self, test_cases: TestCases):
        for i in range(1, 6):
            self.click(locator=locators.ADD_ANSWER_BUTTON)
            assert self.wait_until_true(
                lambda: len(self.find_all(locators.ANSWER_INPUT)) == 2 + i
            )

        with pytest.raises(TimeoutException):
            self.find(locators.ADD_ANSWER_BUTTON, timeout=1)

        for i, remove_locator in zip(range(1, 6), self.find_all(locators.ANSWER_REMOVE)[-1::-1]):
            self.click(elem=remove_locator)
            assert self.wait_until_true(
                lambda: len(self.find_all(locators.ANSWER_INPUT)) == 7 - i
            )

        for answer_input in self.find_all(locators.ANSWER_INPUT):
            self.update_input_field('1', input=answer_input)

        for new_value, expected_value, expected_error in test_cases:
            _, curr_value = self.update_input_field(
                new_value,
                locator=locators.ANSWER_INPUT,
            )

            if expected_value:
                curr_value == expected_value

            if expected_error is None:
                with pytest.raises(TimeoutException):
                    self.wait_until_visible(
                        locators.QUESTIONS_ERROR_ICON(1),
                        timeout=0.1,
                    )
            else:
                assert self.wait_until_visible(locators.QUESTIONS_ERROR_ICON(1))\
                    .is_displayed()

        self.scroll_to(locators.QUESTION_TYPE_BUTTON)
        self.click(locator=locators.QUESTION_TYPE_BUTTON)
        assert self.wait_until_visible(locators.QUESTION_TYPE_FLOATING_TOOLTIP)\
            .is_displayed()

        self.click(locator=locators.FREE_FORM_ANSWER_BUTTON)

        with pytest.raises(TimeoutException):
            self.wait_until_visible(locators.ANSWER_INPUT, timeout=0.5)

    def check_contact_info(self):
        assert self.wait_until_visible(locators.FIRST_NAME_DELETE_BUTTON)\
            .is_displayed()
        assert self.wait_until_visible(locators.PHONE_DELETE_BUTTON)\
            .is_displayed()

        self.click(locator=locators.FIRST_NAME_DELETE_BUTTON)
        self.click(locator=locators.PHONE_DELETE_BUTTON)

        assert self.wait_until_visible(locators.ERROR_BANNER).is_displayed()

        self.click(locator=locators.ADD_CONTACT_INFO_BUTTON)

        assert self.wait_until_visible(locators.CONTACT_INFO_MODAL)\
            .is_displayed()

        self.click(locator=locators.FIRST_NAME_BUTTON)
        self.click(locator=locators.SUBMIT_ADD_CONTACT_INFO_BUTTON)

        assert self.wait_until_visible(locators.FIRST_NAME_DELETE_BUTTON)\
            .is_displayed()

    def complete_second_step(self):
        self.complete_first_step()

        self.press_submit()

    def check_header(self, test_cases: TestCases):
        prev_header, _ = self.update_input_field(
            '',
            locator=locators.HEADER_INPUT,
        )
        self.press_submit()
        self._check_input(
            locators.HEADER_BLOCK,
            locators.HEADER_INPUT,
            test_cases,
            preview_check=lambda text: self.wait_until_visible(
                locators.PREVIEW_TAG('h2', text)
            ).is_displayed(),
            save_after_test_case=False,
        )
        self.update_input_field(prev_header, locator=locators.HEADER_INPUT)

    def check_description(self, test_cases: TestCases):
        prev_header, _ = self.update_input_field(
            '',
            locator=locators.HEADER_INPUT,
        )
        self._check_input(
            locators.DESCRIPTION_BLOCK,
            locators.DESCRIPTION_INPUT,
            test_cases,
        )
        self.update_input_field(prev_header, locator=locators.HEADER_INPUT)

    def check_add_site(self, test_cases: TestCases):
        prev_header, _ = self.update_input_field(
            '',
            locator=locators.HEADER_INPUT,
        )

        self.click(locator=locators.ADD_SITE_BUTTON)

        self._check_input(
            locators.SITE_BLOCK,
            locators.SITE_INPUT,
            test_cases,
        )
        self.update_input_field(prev_header, locator=locators.HEADER_INPUT)

    def check_add_phone(self, test_cases: TestCases):
        prev_header, _ = self.update_input_field(
            '',
            locator=locators.HEADER_INPUT,
        )
        self.click(locator=locators.ADD_PHONE_BUTTON)

        self._check_input(
            locators.PHONE_BLOCK,
            locators.PHONE_INPUT,
            test_cases,
        )
        self.update_input_field(prev_header, locator=locators.HEADER_INPUT)

    def check_add_promo_code(self, test_cases: TestCases):
        prev_header, _ = self.update_input_field(
            '',
            locator=locators.HEADER_INPUT,
        )
        self.click(locator=locators.ADD_PROMO_CODE_BUTTON)

        self._check_input(
            locators.PROMO_CODE_BLOCK,
            locators.PROMO_CODE_INPUT,
            test_cases,
        )
        self.update_input_field(prev_header, locator=locators.HEADER_INPUT)
