import pytest
import allure
from allure_commons.types import AttachmentType
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform").lower()

    if platform == "android":
        options = UiAutomator2Options()
        # Updated with your specific AVD name from the SDK list
        options.device_name = "Pixel_6_Pro_API_36_for_test_Easy-fin"
        options.app = "C:/Users/n.krotsik/Desktop/EasyFin-Android/easy-fin-android/app/build/outputs/apk/debug/app-debug.apk"  # Ensure this path is correct
        options.automation_name = "UIAutomator2"
    else:
        options = XCUITestOptions()
        options.app = "path/to/app.ipa"
        options.device_name = "iPhone_15"

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--platform", action="store", default="android")

# This hook captures the screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Check if the test failed during the 'call' phase
    if rep.when == "call" and rep.failed:
        try:
            # Check if 'driver' exists in the test fixtures
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                # Attach the screenshot to the Allure report
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=AttachmentType.PNG
                )
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")