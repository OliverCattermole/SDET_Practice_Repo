import pytest
from playwright.sync_api import Page, expect

# The 'page' fixture is automatically provided by pytest-playwright
# It represents a single browser tab/page.

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_e2e_scenario(page: Page):
    """
    e2e Test
    """
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    login_page.navigate()
    login_page.login_and_expect_success("standard_user", "secret_sauce")  # Uses the new robust method
    print("\nSuccessful login verified using robust Page Object Model.")
    page.screenshot(path="successful_login_pom.png")
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()
    page.screenshot(path="cart_page.png")
    cart_page.go_to_checkout()
    checkout_page.fill_user_info("Fname", "Lname", "GG1 9AA")
    checkout_page.continue_to_checkout_two()

