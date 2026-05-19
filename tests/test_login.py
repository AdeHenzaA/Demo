import re
import allure
from playwright.sync_api import Page, expect

# Menggunakan dekorator Allure untuk kustomisasi tampilan dasbor
@allure.title("Pengujian Alur Login Utama Saucedemo")
def test_example(page: Page) -> None:
    page.goto("https://saucedemo.com")
    page.locator('[data-test="username"]').click()
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').click()
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    expect(page.locator('[data-test="title"]')).to_contain_text("Products")
