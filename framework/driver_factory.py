import os
import logging
from framework.driver.android_driver import AndroidDriver
from framework.driver.ios_driver import IOSDriver

logger = logging.getLogger(__name__)


class DriverFactory:
    DEFAULT_APPIUM_URL = "http://127.0.0.1:4723"

    @staticmethod
    def resolve_appium_url(config: dict) -> str:
        return (
            config.get("appium_url")
            or os.getenv("APPIUM_URL")
            or DriverFactory.DEFAULT_APPIUM_URL
        )

    @staticmethod
    def get_driver(platform: str, env_config: dict):
        logger.info(f"Initializing driver for platform: {platform}")

        appium_url = DriverFactory.resolve_appium_url(env_config)

        if platform == "android":
            return AndroidDriver.create_driver(env_config, appium_url)

        if platform == "ios":
            return IOSDriver.create_driver(env_config, appium_url)

        raise ValueError(
            f"Unsupported platform '{platform}'. Use 'android' or 'ios'."
        )

