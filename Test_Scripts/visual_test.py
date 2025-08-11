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
    """
    We can mask elements on the screen that we do not want to include in the screenshot, as they may change. E.g. if
    you add an item to the basket, the icon would change. Similar story for advertisements that may be on the page.
    We mask as many elements as we want in the list
    """
    assert_snapshot(page.screenshot(mask=[inventory_page.shopping_cart_icon, inventory_page.sort_dropdown]), threshold=0.8)
