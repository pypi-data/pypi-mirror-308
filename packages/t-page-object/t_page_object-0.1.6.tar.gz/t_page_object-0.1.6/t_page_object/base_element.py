"""Contains the BaseElement class."""
import datetime
import os

from .bot_config import BotConfig
from .utils.logger import logger
from retry import retry
from selenium.common import (  # type: ignore
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidSessionIdException,
    NoSuchElementException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
)

from t_bug_catcher import attach_file_to_exception  # type: ignore
from .bug_catcher_meta import BugCatcherMeta
from .selenium_manager import SeleniumManager
from typing import Callable, TypeVar, Optional, Any

T = TypeVar("T", bound="BaseElement")


def _capture_screenshot_if_error(func: Callable) -> Callable:
    """Decorator to capture screenshot if error occurs."""

    def wrapper(self: T, *args, **kwargs) -> Callable:
        try:
            return func(self, *args, **kwargs)
        except Exception as exception:
            ts = datetime.datetime.now().strftime("%H_%M_%S")
            file_name = f"{self.__class__.__name__}_{func.__name__}_{ts}.png"
            file_path = os.path.join(BotConfig.output_folder, file_name)
            try:
                self.browser.capture_page_screenshot(file_path)
                logger.info(f"Screenshot saved to {file_path}")
                attach_file_to_exception(exception, file_path)
            except (NoSuchWindowException, InvalidSessionIdException) as ex:
                logger.warning(f"Failed to capture screenshot due to error : {str(ex)}")
            raise exception

    return wrapper


class BaseElement(metaclass=BugCatcherMeta):
    """This is an Element used to build each Page."""

    def __init__(self, xpath: str, wait: bool = True, id: str = "", timeout: Optional[int] = None) -> None:
        """
        Initializes a base element with specified parameters.

        Args:
            xpath (str): The XPath expression used to locate the element,
                could also be a formattable string for dynamic XPaths.
            wait (bool, optional): Wait for the element to be present. Defaults to True.
            id (str, optional): An optional identifier for the element. Defaults to None.
            timeout (int, optional): The maximum time to wait for the element to be present, in seconds.

        """
        self.xpath = xpath
        self.wait = wait
        self.id = id
        self.timeout = timeout
        self.original_xpath = xpath
        self.browser = SeleniumManager.get_instance()

    @_capture_screenshot_if_error
    @retry(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            NoSuchElementException,
            ElementNotInteractableException,
            AssertionError,
            TimeoutException,
        ),
        tries=2,
        delay=1,
    )
    def format_xpath(self, *args: list, **kwargs: dict) -> None:
        """If using a dynamic xpath, this method formats the xpath string.

        Args:
            *args (list): The arguments to be used to format the xpath.
            **kwargs (dict): The keyword arguments to be used to format the
        """
        self.xpath = self.original_xpath.format(*args, **kwargs)

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Delegate method calls not found in this class to the Selenium instance."""
        if self.browser.get_browser_ids():
            if not self.wait_element_load():
                logger.info(f"Element not found: {self.xpath}. Wait is set to False. Doing nothing")
                return lambda *args, **kwargs: None
            return lambda *args, **kwargs: self._selenium_method(name, *args, **kwargs)
        return None  # type: ignore

    def _selenium_method(self, name: str, *args, **kwargs) -> Callable:
        """Executing self.browser.name(*args,**kwargs) method.

        For example: self.browser.click_element(self.xpath)
        """
        method = getattr(self.browser, name, None)
        if method:
            return method(self.xpath, *args, **kwargs)
        else:
            raise AttributeError(f"Method '{name}' not found in Selenium instance.")

    @_capture_screenshot_if_error
    @retry(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            NoSuchElementException,
            ElementNotInteractableException,
            AssertionError,
            TimeoutException,
        ),
        tries=2,
        delay=1,
    )
    def wait_element_load(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for element to load.

        Args:
            timeout (int, optional): The maximum time to wait for the element to be present, in seconds.
                Defaults to None. Overwrites apps inherent timeout if set.

        Returns:
            bool: True if element is visible, False not found and wait is False otherwise.

        Raises:
            AssertionError: If element is not visible and wait is True.
        """
        try:
            if timeout:
                self.browser.wait_until_element_is_visible(self.xpath, timeout=timeout)
            elif self.timeout:
                self.browser.wait_until_element_is_visible(self.xpath, timeout=self.timeout)
            else:
                self.browser.wait_until_element_is_visible(self.xpath)
        except AssertionError as e:
            if self.wait:
                raise e
            return False
        return True
