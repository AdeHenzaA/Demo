import allure
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@allure.epic("Web Application Testing")
@allure.feature("Authentication & Navigation")
@allure.story("User Login and Redirect to About Page")
@allure.title("Successful Login and Navigate to Sauce Labs Home")
@allure.description(
    "Verify that a standard user can successfully log in to Saucedemo, "
    "open the sidebar menu, click the About link, and be successfully "
    "redirected to the official Sauce Labs landing page."
)
def test_login_and_navigate_to_about(page: Page) -> None:
    # Inisialisasi Page Objects
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    # Langkah 1: Buka Website & Login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # Langkah 2: Navigasi Menu Dashboard (dari codegen)
    dashboard_page.open_menu()
    dashboard_page.click_about()

    # Langkah 3: Validasi Akhir
    dashboard_page.verify_saucelabs_home_visible()