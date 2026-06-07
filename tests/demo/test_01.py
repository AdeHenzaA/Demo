import re
from playwright.sync_api import Page, expect
import allure

@allure.severity(allure.severity_level.CRITICAL) #BLOCKER ,CRITICAL ,NORMAL ,MINOR ,TRIVIAL 
@allure.feature("Login Tests")          
@allure.story("Negative & Positive Login")     
@allure.title("Saucedemo Login verification") 
@allure.description("""
An interactive test scenario to validate the Swag Labs login page.
The test includes:
1. Failed login with an incorrect password
2. Failed login with an incorrect username
3. Validation error for an empty form (username & password)
4. Successful login to the main dashboard page
""") 

def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    with allure.step("Failed login with an incorrect password"):
        page.locator("[data-test=\"username\"]").click()
        page.locator("[data-test=\"username\"]").fill("standard_user")
        page.locator("[data-test=\"password\"]").click()
        page.locator("[data-test=\"password\"]").fill("demo")
        page.locator("[data-test=\"login-button\"]").click()
        expect(page.locator("[data-test=\"error\"]")).to_be_visible()
    with allure.step("Failed login with an incorrect username"):
        page.locator("[data-test=\"username\"]").click()
        page.locator("[data-test=\"username\"]").fill("standard_user11")
        page.locator("[data-test=\"password\"]").click()
        page.locator("[data-test=\"password\"]").fill("secret_sauce")
        page.locator("[data-test=\"login-button\"]").click()
        expect(page.locator("[data-test=\"error\"]")).to_be_visible()
    with allure.step("Failed login with an incorrect username"):
        page.locator("[data-test=\"username\"]").click()
        page.locator("[data-test=\"username\"]").fill("")
        page.locator("[data-test=\"password\"]").click()
        page.locator("[data-test=\"password\"]").fill("")
        page.locator("[data-test=\"login-button\"]").click()
        expect(page.locator("div").filter(has_text=re.compile(r"^Epic sadface: Username is required$"))).to_be_visible()
        page.locator("[data-test=\"username\"]").click()
        page.locator("[data-test=\"username\"]").fill("standard_user")
        page.locator("[data-test=\"login-button\"]").click()
        expect(page.locator("div").filter(has_text=re.compile(r"^Epic sadface: Password is required$"))).to_be_visible()
    with allure.step("Successful login to the main dashboard page"):
        page.locator("[data-test=\"password\"]").click()
        page.locator("[data-test=\"password\"]").fill("secret_sauce")
        page.locator("[data-test=\"login-button\"]").click()
        expect(page.get_by_text("ProducSSppS")).to_be_visible()
