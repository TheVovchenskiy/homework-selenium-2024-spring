import time
import pytest
from _pytest.fixtures import FixtureRequest

from base import LoginCase
from ui.pages.settings_page import SettingsPage

from ui.fixtures import *


class SettingsCase(LoginCase):
    def settings_setup(self):
        self.main_page.go_to_settings()
        self.settings_page = SettingsPage(self.driver)


class TestSettings(SettingsCase):
    def test_base(self):
        time.sleep(2)
        assert 1 == 1
