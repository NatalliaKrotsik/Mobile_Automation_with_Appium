from appium import webdriver
from appium.options.ios import XCUITestOptions


class IOSDriver:
    REQUIRED_KEYS = ["device_name", "app"]

    @staticmethod
    def validate_config(config: dict):
        missing = [
            key for key in IOSDriver.REQUIRED_KEYS
            if key not in config
        ]
        if missing:
            raise ValueError(f"Missing required iOS config keys: {missing}")

    @staticmethod
    def create_driver(config: dict, appium_url: str):
        IOSDriver.validate_config(config)

        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.automation_name = "XCUITest"
        options.device_name = config["device_name"]
        options.app = config["app"]

        return webdriver.Remote(appium_url, options=options)

