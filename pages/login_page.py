import allure
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Elemen halaman Login
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')
        
        # Elemen halaman Dashboard (untuk validasi login sukses)
        self.app_logo = page.locator('.app_logo')
        self.inventory_container = page.locator('[data-test="inventory-container"]')

    @allure.step("Navigate to Saucedemo website")
    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    @allure.step("Login with username '{username}' and password '{password}'")
    def login(self, username: str, password: str):
        # Menyimpan parameter ke Allure Report
        allure.dynamic.parameter("username", username)
        allure.dynamic.parameter("password", password)
        
        self.username_input.click()
        self.username_input.fill(username)
        self.password_input.click()
        self.password_input.fill(password)
        self.login_button.click()

    @allure.step("Verify error message contains text: {expected_text}")
    def verify_error_message(self, expected_text: str):
        allure.dynamic.parameter("expected_error_text", expected_text)
        # Assertion berjalan alami tanpa try-except
        expect(self.error_message).to_contain_text(expected_text)

    @allure.step("Verify login success by checking dashboard elements")
    def verify_login_success(self):
        # Memastikan logo atau container produk muncul setelah login berhasil
        expect(self.app_logo).to_be_visible()
        expect(self.inventory_container).to_be_visible()