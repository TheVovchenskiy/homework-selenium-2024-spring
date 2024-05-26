import time
from typing import Optional
from selenium.common.exceptions import TimeoutException

from base import LoginCase
from ui.locators.base_locators import Locator
from ui.locators.lead_form_locators import LeadFormLocators as locators
from ui.pages.lead_form_page import (
    LeadFormPage,
    ERR_MAX_FIELD_LEN,
    ERR_REQUIRED_FIELD,
    ERR_MAX_NEW_LINE_COUNT,
    ERR_VALUE_GT_ZERO,
    ERR_MAX_DISCOUNT_PERCENT
)

from ui.fixtures import *


class LeadFormCase(LoginCase):
    def lead_form_setup(self):
        self.lead_form_page = LeadFormPage(self.driver)
        self.lead_form_page.wait_until_loaded([
            locators.CREATE_BUTTON,
        ])


class TestLeadForm(LeadFormCase):
    def test_first_step(self):
        self.lead_form_page.open_create_lead_form()

        self.lead_form_page.check_lead_form_name_input([
            ('', None, ERR_REQUIRED_FIELD),
            ('    ', None, ERR_REQUIRED_FIELD),
            ('c' * 256, None, ERR_MAX_FIELD_LEN),
            ('lead form name', None, None),
        ])

        self.lead_form_page.check_upload_logo()

        self.lead_form_page.check_company_name_input([
            ('', None, ERR_REQUIRED_FIELD),
            ('     ', None, ERR_REQUIRED_FIELD),
            ('c' * 31, None, ERR_MAX_FIELD_LEN),
            ('company name', None, None),
        ])

        self.lead_form_page.check_compact(
            [
                ('', None, ERR_REQUIRED_FIELD),
                ('    ', None, ERR_REQUIRED_FIELD),
                ('c' * 51, None, ERR_MAX_FIELD_LEN),
                ('header', None, None),
            ],
            [
                ('', None, ERR_REQUIRED_FIELD),
                ('    ', None, ERR_REQUIRED_FIELD),
                ('c' * 36, None, ERR_MAX_FIELD_LEN),
                ('short description', None, None),
            ],
        )

        self.lead_form_page.check_long(
            [
                ('', None, ERR_REQUIRED_FIELD),
                ('    ', None, ERR_REQUIRED_FIELD),
                ('c' * 51, None, ERR_MAX_FIELD_LEN),
                ('header', None, None),
            ],
            [
                ('', None, ERR_REQUIRED_FIELD),
                ('    ', None, ERR_REQUIRED_FIELD),
                ('c' * 351, None, ERR_MAX_FIELD_LEN),
                ('first line\n\n\nsecond line', None, ERR_MAX_NEW_LINE_COUNT),
                ('long description', None, None),
            ],
        )

        self.lead_form_page.check_award(
            [
                ('', '0', ERR_VALUE_GT_ZERO),
                ('   ', '0', ERR_VALUE_GT_ZERO),
                ('abc', '0', ERR_VALUE_GT_ZERO),
                ('1abc2', '12', None),
                ('12', '12', None),
                ('999999999999', '999999999999', None),
                ('9999999999999', '999999999999', None),
            ],
            [
                ('', '0', ERR_VALUE_GT_ZERO),
                ('   ', '0', ERR_VALUE_GT_ZERO),
                ('abc', '0', ERR_VALUE_GT_ZERO),
                ('1abc2', '12', None),
                ('12', '12', None),
                ('999999999999', '999999999999', ERR_MAX_DISCOUNT_PERCENT),
                ('9999999999999', '999999999999', ERR_MAX_DISCOUNT_PERCENT),
            ],
            [
                ('', None, ERR_REQUIRED_FIELD),
                ('  ', None, ERR_REQUIRED_FIELD),
                ('c' * 31, None, ERR_MAX_FIELD_LEN),
                ('bonus', None, None),
            ],
        )
