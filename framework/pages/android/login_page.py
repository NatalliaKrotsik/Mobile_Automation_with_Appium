from appium.webdriver.common.appiumby import AppiumBy
from framework.base_page import BasePage

class AndroidLoginPage(BasePage):
    # Using Accessibility IDs as we discussed
    EMAIL_FIELD = (AppiumBy.ACCESSIBILITY_ID, "input_email")
    LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "btn_login")

    def login_as(self, email):
        self.fill(self.EMAIL_FIELD, email)
        self.click(self.LOGIN_BTN)