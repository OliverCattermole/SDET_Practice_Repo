from playwright.sync_api import Playwright, sync_playwright, expect
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# def test_visual_landing(page, assert_snapshot):
#     page.goto("https://www.saucedemo.com/")
#     assert_snapshot(page.screenshot())

def test_visual_landing_2(page, assert_snapshot):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    login_page.navigate()
    login_page.login_and_expect_success("standard_user", "secret_sauce")  # Uses the new robust method

    # Masking elements that change frequently (cart count, dynamic ads, etc.) to prevent false baseline failures.
    assert_snapshot(
        page.screenshot(mask=[inventory_page.shopping_cart_icon, inventory_page.sort_dropdown]),
        threshold=0.8
    )
