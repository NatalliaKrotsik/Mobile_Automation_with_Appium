import logging
import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_clickable(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_visible(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Clicking element: {locator}")
    def click_element(self, locator):
        logger.info(f"Attempting to click: {locator}")
        self.wait_for_clickable(locator).click()

    @allure.step("Entering text '{text}' into {locator}")
    def enter_text(self, locator, text):
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait_for_visible(locator).text

    def is_element_visible(self, locator, timeout=5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False