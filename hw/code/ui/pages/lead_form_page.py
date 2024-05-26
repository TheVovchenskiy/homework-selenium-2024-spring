import os
from typing import Any, Callable
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

    def expect_error(self, expected_error: str | None, block_locator: Locator) -> bool:
        if expected_error is None:
            try:
                existing_error = self.get_error(block_locator, 0.5)
            except TimeoutException:
                return True
            else:
                return False

        existing_error = self.get_error(block_locator, 1)
        if expected_error in existing_error.text:
            return True

        return False

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
    ):
        prev_value = self.get_input_value(locator=input_locator)
        for new_value, expected_value, expected_error in test_cases:
            _, curr_value = self.update_input_field(
                new_value,
                locator=input_locator,
            )

            if expected_value:
                curr_value == expected_value

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
        self.check_award_discount(
            discount_money_test_cases,
            discount_percent_test_cases,
        )

        self.check_award_bonus(bonus_test_cases)

    def check_award_discount(
        self,
        money_test_cases: TestCases,
        percent_test_cases: TestCases,
    ):
        self.scroll_to(locators.DISCOUNT_RADIOBUTTON)
        discount_button = self.wait_until_visible(locators.DISCOUNT_BUTTON)
        self.click(elem=discount_button)
        assert self.find(locators.DISCOUNT_RADIOBUTTON).is_selected()

        self.check_award_discount_money(money_test_cases)
        self.check_award_discount_percent(percent_test_cases)

    def check_award_discount_money(self, test_cases: TestCases):
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

    def check_award_discount_percent(self, test_cases: TestCases):
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

    def check_award_bonus(
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
