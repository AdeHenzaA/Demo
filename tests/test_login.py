import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage

@allure.epic("Authentication Management")
@allure.feature("Login Feature")
class Test_LoginScenario:

    @allure.story("Positive Login Scenario")
    @allure.title("Login with Valid Credentials")
    @allure.description("Verifying that the user can successfully login with standard valid credentials.")
    def test_login_success(self, page: Page):
        login_page = LoginPage(page)
        
        # 1. Step Pengujian
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce") # Kredensial yang benar
        
        # 2. Validasi / Expected & Actual Result
        login_page.verify_login_success()

    @allure.story("Negative Login Scenarios")
    @allure.title("Login with Invalid Username")
    @allure.description("Verifying the application behavior when login fails due to an invalid username.")
    def test_login_invalid_username(self, page: Page):
        login_page = LoginPage(page)
        
        # 1. Step Pengujian
        login_page.navigate()
        login_page.login("baksi", "secret_sauce")
        
        # 2. Validasi / Expected & Actual Result
        login_page.verify_error_message("Epic sadface: Username and password do not match any user in this service")

    @allure.story("Negative Login Scenarios")
    @allure.title("Login with Invalid Password")
    @allure.description("Verifying the application behavior when login fails due to an incorrect password.")
    def test_login_invalid_password(self, page: Page):
        login_page = LoginPage(page)
        
        # 1. Step Pengujian
        login_page.navigate()
        login_page.login("standard_user", "baksooo")
        
        # 2. Validasi / Expected & Actual Result
        login_page.verify_error_message("Epic sadface: Username and password do not match any user in this service")