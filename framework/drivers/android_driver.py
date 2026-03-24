from appium import webdriver
from appium.options.android import UiAutomator2Options


class AndroidDriver:
    REQUIRED_KEYS = ["device_name", "app", "app_package"]

    @staticmethod
    def validate_config(config: dict):
        missing = [
            key for key in AndroidDriver.REQUIRED_KEYS
            if key not in config
        ]
        if missing:
            raise ValueError(f"Missing required Android config keys: {missing}")

    @staticmethod
    def create_driver(config: dict, appium_url: str):
        AndroidDriver.validate_config(config)

        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UIAutomator2"
        options.device_name = config["device_name"]
        options.app = config["app"]
        options.app_package = config["app_package"]
        options.app_wait_activity = config.get("app_wait_activity", "*")

        return webdriver.Remote(appium_url, options=options)

