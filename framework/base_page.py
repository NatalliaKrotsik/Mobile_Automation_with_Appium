import logging
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    @allure.step("Clicking element: {locator}")
    def click_element(self, locator):
        logger.info(f"Attempting to click: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Entering text '{text}' into {locator}")
    def enter_text(self, locator, text):
        logger.info(f"Entering '{text}' into element: {locator}")
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        logger.info(f"Getting text from: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator)).text