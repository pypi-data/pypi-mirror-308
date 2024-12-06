#!/usr/bin/env python
"""Tests for ui component methods."""
from .t_test_app import TestApp
from t_object import ThoughtfulObject
import os


class Article(ThoughtfulObject):
    """Article class."""

    title: str = ""
    category: str = ""


class TestMethods:
    """Test UI methods."""

    @classmethod
    def setup_class(self):
        """Setup class."""
        self.remote_url = os.getenv("SELENIUM_GRID_URL")

        # We need this var for bitbucket pipelines sucessfull run
        self.executable_path = os.path.join(os.getcwd(), "chromedriver")
        if not os.path.exists(self.executable_path):
            self.executable_path = None

    def setup_method(self):
        """Setup method."""
        self.app = TestApp()

    def teardown_method(self):
        """Teardown method."""
        self.app.browser.close_browser()

    def test_ui_elements(self):
        """Test UI elements in browser instance."""
        self.app.browser.open_browser(
            browser="chrome",
            url=self.app.test_page.url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.app.test_page.visit()
        self.app.test_page.continue_button.format_xpath(name="Continue")
        self.app.test_page.continue_button.click()
        self.app.test_page.search_button.click()
        self.app.test_page.search_input.input_text_and_check("robot")
        self.app.test_page.search_go.click()
        self.app.test_page.image.download_image()
        self.app.test_page.article.get_text_values(Article)
        self.app.test_page.section_button.click()
        self.app.test_page.arts_cb.select()
        self.app.test_page.sort_by_dd.click_and_select_option("Sort by Newest", option_tag="option")
