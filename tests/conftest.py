import os
import pytest
from core.driver_factory import DriverFactory
from config.config_loader import load_config

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="env to run tests against")

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function")
def setup(page, request):
    """
    Use pytest-playwright's `page` fixture.
    Attaches a DriverFactory wrapper as `page.driver` and navigates to base_url if provided.
    """
    env = request.config.getoption("--env", "dev")
    config = load_config(env) or {}

    # attach driver wrapper and config
    driver = DriverFactory(page, config)
    page.driver = driver
    page.config = config

    # apply config defaults
    page.set_default_timeout(config.get("timeout", 30000))

    base_url = config.get("base_url")
    if base_url:
        page.goto(base_url)

    yield page

    # teardown: capture screenshot on failure
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        os.makedirs("reports/failures", exist_ok=True)
        try:
            page.screenshot(path=f"reports/failures/{request.node.name}.png")
        except Exception:
            pass