from appium.webdriver.common.appiumby import AppiumBy
from framework.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    # LOCATORS
    # 1. The initial "Log In" button on the welcome/splash screen
    START_LOGIN_BUTTON = (AppiumBy.XPATH, '(//android.widget.Button)[2]')

    # 2. The fields on the actual login form
    PESEL_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@password='false']")
    PASSWORD_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@password='true']")

    def click_start_login(self):
        self.click_element(self.START_LOGIN_BUTTON)

    def is_login_form_displayed(self):
        try:
            pesel = self.wait.until(EC.visibility_of_element_located(self.PESEL_FIELD))
            password = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            return pesel.is_displayed() and password.is_displayed()
        except:
            return False