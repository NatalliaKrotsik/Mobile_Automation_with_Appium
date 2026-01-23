import pytest
import allure
import logging
from allure_commons.types import AttachmentType
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform").lower()
    logger.info(f"Initializing driver for platform: {platform}")

    if platform == "android":
        options = UiAutomator2Options()
        options.device_name = "Pixel_6_Pro_API_36_for_test_Easy-fin"
        # Use quotes for Windows paths with spaces or special characters
        options.app = "C:/Users/n.krotsik/Desktop/EasyFin-Android/easy-fin-android/app/build/outputs/apk/debug/app-debug.apk"
        options.automation_name = "UIAutomator2"
    else:
        options = XCUITestOptions()
        options.app = "path/to/app.ipa"
        options.device_name = "iPhone_15"

    driver = webdriver.Remote("http://localhost:4723", options=options)

    # Trace connection success
    logger.info("Appium driver session created successfully")

    yield driver

    logger.info("Closing driver session")
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--platform", action="store", default="android")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                # Capture screenshot
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=AttachmentType.PNG
                )
                # Also capture Logcat for better tracing
                logcat = driver.get_log("logcat")[-50:]  # Get last 50 lines
                allure.attach(
                    str(logcat),
                    name="android_logcat_trace",
                    attachment_type=AttachmentType.TEXT
                )
        except Exception as e:
            logger.error(f"Failed to capture failure artifacts: {e}")