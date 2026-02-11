from appium.webdriver.common.appiumby import AppiumBy
from framework.base_page import BasePage


class LoginPage(BasePage):

    # Better to replace XPath later (see below)
    START_LOGIN_BUTTON = (AppiumBy.XPATH, '(//android.widget.Button)[2]')
    PESEL_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@password='false']")
    PASSWORD_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@password='true']")

    def click_start_login(self):
        self.click_element(self.START_LOGIN_BUTTON)

    def is_login_form_displayed(self) -> bool:
        pesel_visible = self.is_element_visible(self.PESEL_FIELD, timeout=10)
        password_visible = self.is_element_visible(self.PASSWORD_FIELD, timeout=10)
        return pesel_visible and password_visible
