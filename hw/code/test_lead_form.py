import time
from typing import Optional
from selenium.common.exceptions import TimeoutException
import allure

from base import LoginCase
from ui.locators.base_locators import Locator
from ui.locators.lead_form_locators import LeadFormLocators as locators
from ui.pages.lead_form_page import (
    LeadFormPage,
    ERR_MAX_FIELD_LEN,
    ERR_REQUIRED_FIELD,
    ERR_MAX_NEW_LINE_COUNT,
    ERR_VALUE_GT_ZERO,
    ERR_MAX_DISCOUNT_PERCENT,
    ERR_INVALID_URL,
    ERR_INVALID_PHONE,
    ERR_INVALID_EMAILS,
    ERR_INVALID_EMAIL,
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

    def test_second_step(self):
        self.lead_form_page.complete_first_step()

        self.lead_form_page.check_question(
            [
                ('', '', 'error'),
                ('   ', '    ', 'error'),
                ('c' * 69, 'c' * 68, None),
                ('question', 'question', None),
            ],
            [
                ('', '', 'error'),
                ('   ', '    ', 'error'),
                ('c' * 41, 'c' * 41, None),
                ('answer', 'answer', None),
            ],
        )

        self.lead_form_page.check_contact_info()

    def test_third_step(self):
        self.lead_form_page.complete_second_step()

        self.lead_form_page.check_header([
            ('', None, ERR_REQUIRED_FIELD),
            ('    ', None, ERR_REQUIRED_FIELD),
            ('c' * 26, None, ERR_MAX_FIELD_LEN),
            ('header', None, None),
        ])

        self.lead_form_page.check_description([
            ('', None, None),
            ('    ', None, None),
            ('c' * 161, None, ERR_MAX_FIELD_LEN),
            ('description', None, None),
        ])

        self.lead_form_page.check_add_site([
            ('', None, None),
            ('    ', None, ERR_INVALID_URL),
            ('example.com', None, ERR_INVALID_URL),
            ('https://example.com', None, None),
        ])

        self.lead_form_page.check_add_phone([
            ('', None, None),
            ('    ', None, ERR_INVALID_PHONE),
            ('89608363276', None, ERR_INVALID_PHONE),
            ('abc', None, ERR_INVALID_PHONE),
            ('+71234567890', None, None),
        ])

        self.lead_form_page.check_add_promo_code([
            ('', None, None),
            ('    ', None, None),
            ('a' * 31, None, ERR_MAX_FIELD_LEN),
            ('some promo code', None, None),
        ])

    def test_fourth_step(self):
        self.lead_form_page.complete_third_step()

        self.lead_form_page.check_emails([
            ('', None, None),
            ('    ', None, None),
            ('email@example', None, ERR_INVALID_EMAILS),
            ('e@@e.com', None, ERR_INVALID_EMAILS),
            ('e@e..com', None, ERR_INVALID_EMAILS),
            ('em..ail@e.com', None, ERR_INVALID_EMAILS),
            ('@example.com', None, ERR_INVALID_EMAILS),
            ('email', None, ERR_INVALID_EMAILS),
            ('@', None, ERR_INVALID_EMAILS),
            ('email', None, ERR_INVALID_EMAILS),
            ('em<ail@e.com', None, ERR_INVALID_EMAILS),
            ('em>ail@e.com', None, ERR_INVALID_EMAILS),
            ('em,ail@e.com', None, ERR_INVALID_EMAILS),
            ('em"ail@e.com', None, ERR_INVALID_EMAILS),
            ('em:ail@e.com', None, ERR_INVALID_EMAILS),
            ('em;ail@e.com', None, ERR_INVALID_EMAILS),
            ('em[ail@e.com', None, ERR_INVALID_EMAILS),
            ('em]ail@e.com', None, ERR_INVALID_EMAILS),
            ('em@ail@e.com', None, ERR_INVALID_EMAILS),
            ('ma il@e.com', None, ERR_INVALID_EMAILS),
            ('mail@e<e.com', None, ERR_INVALID_EMAILS),
            ('mail@e>e.com', None, ERR_INVALID_EMAILS),
            ('mail@e,e.com', None, ERR_INVALID_EMAILS),
            ('mail@e"e.com', None, ERR_INVALID_EMAILS),
            ('mail@e:e.com', None, ERR_INVALID_EMAILS),
            ('mail@e;e.com', None, ERR_INVALID_EMAILS),
            ('mail@e[e.com', None, ERR_INVALID_EMAILS),
            ('mail@e]e.com', None, ERR_INVALID_EMAILS),
            ('mail@e@e.com', None, ERR_INVALID_EMAILS),
            ('mail@e e.com', None, ERR_INVALID_EMAILS),
            ('email@example.com, email', None, ERR_INVALID_EMAILS),
            ('mail@e.com ', None, None),
            ('email@example.co', None, None),
            ('email@e.c', None, None),
            (' mail@e.com', None, None),
            ('email@e.x.a.m.p.l.e.com', None, None),
            ('email@example.com', None, None),
            ('email@example.com,email@example.com', None, None),
            (' email@example.com , email@example.com ', None, None),
        ])

        self.lead_form_page.check_messenger()

        self.lead_form_page.check_name([
            ('', None, ERR_REQUIRED_FIELD),
            ('   ', None, ERR_REQUIRED_FIELD),
            ('n' * 256, None, ERR_MAX_FIELD_LEN),
            ('name', None, None),
            ('firstname lastname', None, None),
        ])

        self.lead_form_page.check_address([
            ('', None, ERR_REQUIRED_FIELD),
            ('   ', None, ERR_REQUIRED_FIELD),
            ('a' * 256, None, ERR_MAX_FIELD_LEN),
            ('address', None, None),
            ('long address', None, None),
        ])

        self.lead_form_page.check_email([
            ('', None, None),
            ('    ', None, ERR_INVALID_EMAIL),
            ('email@example', None, ERR_INVALID_EMAIL),
            ('e@@e.com', None, ERR_INVALID_EMAIL),
            ('e@e..com', None, ERR_INVALID_EMAIL),
            ('em..ail@e.com', None, ERR_INVALID_EMAIL),
            ('@example.com', None, ERR_INVALID_EMAIL),
            ('email', None, ERR_INVALID_EMAIL),
            ('@', None, ERR_INVALID_EMAIL),
            ('email', None, ERR_INVALID_EMAIL),
            ('em<ail@e.com', None, ERR_INVALID_EMAIL),
            ('em>ail@e.com', None, ERR_INVALID_EMAIL),
            ('em,ail@e.com', None, ERR_INVALID_EMAIL),
            ('em"ail@e.com', None, ERR_INVALID_EMAIL),
            ('em:ail@e.com', None, ERR_INVALID_EMAIL),
            ('em;ail@e.com', None, ERR_INVALID_EMAIL),
            ('em[ail@e.com', None, ERR_INVALID_EMAIL),
            ('em]ail@e.com', None, ERR_INVALID_EMAIL),
            ('em@ail@e.com', None, ERR_INVALID_EMAIL),
            ('ma il@e.com', None, ERR_INVALID_EMAIL),
            ('mail@e<e.com', None, ERR_INVALID_EMAIL),
            ('mail@e>e.com', None, ERR_INVALID_EMAIL),
            ('mail@e,e.com', None, ERR_INVALID_EMAIL),
            ('mail@e"e.com', None, ERR_INVALID_EMAIL),
            ('mail@e:e.com', None, ERR_INVALID_EMAIL),
            ('mail@e;e.com', None, ERR_INVALID_EMAIL),
            ('mail@e[e.com', None, ERR_INVALID_EMAIL),
            ('mail@e]e.com', None, ERR_INVALID_EMAIL),
            ('mail@e@e.com', None, ERR_INVALID_EMAIL),
            ('mail@e e.com', None, ERR_INVALID_EMAIL),
            ('email@example.com, email', None, ERR_INVALID_EMAIL),
            ('mail@e.com ', None, ERR_INVALID_EMAIL),
            (' mail@e.com', None, ERR_INVALID_EMAIL),
            ('email@example.co', None, None),
            ('email@e.c', None, None),
            ('email@e.x.a.m.p.l.e.com', None, None),
            ('email@example.com', None, None),
        ])

        self.lead_form_page.check_inn([
            ('', None, None),
            ('   ', None, None),
            ('a' * 33, None, ERR_MAX_FIELD_LEN),
            ('inn', None, None),
            ('123', None, None),
        ])

    def test_create_delete(self):
        self.lead_form_page.create_and_delete_lead_form()
