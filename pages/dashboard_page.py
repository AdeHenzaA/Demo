import allure
from playwright.sync_api import Page, expect

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.about_link = page.locator('[data-test="about-sidebar-link"]')
        self.saucelabs_home_link = page.get_by_role("link", name="Sauce Labs Home")

    @allure.step("Open sidebar menu")
    def open_menu(self):
        self.menu_button.click()

    @allure.step("Click on About sidebar link")
    def click_about(self):
        self.about_link.click()

    @allure.step("Verify successfully redirected to Sauce Labs Home Page")
    def verify_saucelabs_home_visible(self):
        expect(self.saucelabs_home_link).to_be_visible()