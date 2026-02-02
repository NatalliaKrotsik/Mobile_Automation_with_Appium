import pytest
import allure
import logging
from allure_commons.types import AttachmentType
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# Configure logging to see real-time progress in GitLab CI logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform").lower()
    logger.info(f"🚀 Initializing driver for platform: {platform}")

    if platform == "android":
        options = UiAutomator2Options()
        options.device_name = "Pixel_6"
        # Using forward slashes is safer for Python strings on Windows
        options.app = "C:/Users/n.krotsik/Desktop/EasyFin-Android/easy-fin-android/app/build/outputs/apk/debug/app-debug.apk"
        options.automation_name = "UIAutomator2"

        # --- Stability Fixes for CI ---
        options.app_package = "com.andersenlab.easyfin"
        # Wait for any activity to start (prevents 500 errors on Splash screens)
        options.app_wait_activity = "*"
        # Increase timeout for the app to install and launch on slow emulators
        options.adb_exec_timeout = 60000
        options.android_install_timeout = 90000
    else:
        options = XCUITestOptions()
        options.app = "path/to/app.ipa"
        options.device_name = "iPhone_15"

    # Use 127.0.0.1 instead of localhost to bypass Windows IPv6 resolution issues
    try:
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        logger.info("✅ Appium driver session created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create Appium session: {e}")
        raise e

    yield driver

    logger.info("🧹 Closing driver session")
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

                # 1. Capture Screenshot
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=AttachmentType.PNG
                )

                # 2. Capture and Format Logcat (last 100 lines)
                raw_logs = driver.get_log("logcat")[-100:]
                formatted_logs = "\n".join([
                    f"{log.get('timestamp')} [{log.get('level')}] {log.get('message')}"
                    for log in raw_logs
                ])
                allure.attach(
                    formatted_logs,
                    name="android_logcat_trace",
                    attachment_type=AttachmentType.TEXT
                )

                logger.info("📸 Failure artifacts (screenshot & logcat) attached to Allure")
        except Exception as e:
            logger.error(f"⚠️ Failed to capture failure artifacts: {e}")