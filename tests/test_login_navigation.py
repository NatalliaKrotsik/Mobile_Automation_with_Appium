import pytest
from framework.pages.android.login_page import LoginPage

def test_navigation_to_login_form(driver):
    login_page = LoginPage(driver)

    # Step 1: Click the initial Log In button
    print("Clicking the initial Log In button...")
    login_page.click_start_login()

    # Step 2: Verify that the PESEL and Password fields appear
    print("Verifying if PESEL and Password fields are displayed...")
    assert login_page.is_login_form_displayed(), "Login form with PESEL and Password was not found!"