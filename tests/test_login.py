import pytest
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login(setup):
    page = setup
    page.goto(page.config["base_url"])

    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    assert "inventory" in page.url
