# tests/test_login_scenarios.py (Modified)
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage # Important: import the InventoryPage too

def test_invalid_login_scenario_with_page_object_refactored(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid_user", "wrong_password")
    # Assertions remain in the test function
    expect(login_page.error_message).to_have_text("Epic sadface: Username and password do not match any user in this service")
    print("\nInvalid login error message verified via refactored POM.")

def test_successful_login_scenario_with_page_object_refactored(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    # Use the method that specifically handles successful login and returns the next page
    inventory_page = login_page.login_successfully("standard_user", "secret_sauce")

    # Assertions on the InventoryPage's elements
    expect(inventory_page.products_title).to_be_visible() # Check visibility
    expect(inventory_page.products_title).to_have_text("Products") # Check text
    # Or, if you prefer using a method:
    # assert inventory_page.get_products_title_text() == "Products"

    print("\nSuccessful login verified using refactored Page Object Model.")