import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform").lower()

    if platform == "android":
        options = UiAutomator2Options()
        options.app = "path/to/app.apk"
        options.device_name = "Android_Emulator"
    else:
        options = XCUITestOptions()
        options.app = "path/to/app.ipa"
        options.device_name = "iPhone_15"

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--platform", action="store", default="android")