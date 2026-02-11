import yaml
import pytest
import allure
import logging
from pathlib import Path
from allure_commons.types import AttachmentType
from framework.driver_factory import DriverFactory

logger = logging.getLogger(__name__)


# ----------------------------
# Pytest CLI options
# ----------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Mobile platform: android or ios"
    )
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment: dev / test / prod"
    )


# ----------------------------
# YAML Validation Helper
# ----------------------------
def validate_config(config: dict, required_keys: list):
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing required config keys: {missing}")


# ----------------------------
# Driver fixture
# ----------------------------
@pytest.fixture(scope="function")
def driver(request):
    platform = request.config.getoption("--platform").lower()
    env = request.config.getoption("--env")

    config_path = (
    Path(request.config.rootpath)
    / "config"
    / platform
    / f"{env}.yaml"
)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        env_config = yaml.safe_load(f)

    logger.info(f"🚀 Starting test | platform={platform}, env={env}")

    driver = DriverFactory.get_driver(platform, env_config)

    # Attach capabilities to Allure
    try:
        allure.attach(
            str(driver.capabilities),
            name="driver_capabilities",
            attachment_type=AttachmentType.JSON
        )
    except Exception:
        logger.warning("Could not attach driver capabilities")

    yield driver

    logger.info("🔧 Quitting driver session")
    driver.quit()


# ----------------------------
# Failure hook
# ----------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or not rep.failed:
        return

    if "driver" not in item.funcargs:
        return

    driver = item.funcargs["driver"]
    platform = item.config.getoption("--platform").lower()

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=AttachmentType.PNG
        )

        if platform == "android":
            logs = driver.get_log("logcat")[-100:]
            formatted_logs = "\n".join(
                f"{log['timestamp']} [{log['level']}] {log['message']}"
                for log in logs
            )
            allure.attach(
                formatted_logs,
                name="android_logcat",
                attachment_type=AttachmentType.TEXT
            )

        logger.info("📸 Failure artifacts attached to Allure")

    except Exception as e:
        logger.error(f"⚠️ Failed to collect failure artifacts: {e}")
