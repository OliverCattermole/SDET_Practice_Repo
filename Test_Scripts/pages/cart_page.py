# pages/cart_page.py
from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage

class CartPage(BasePage):
    """
    Page Object for the cart page.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators (using Playwright's recommended locators where possible)
        self.continue_shopping = page.get_by_role("button", name="continue-shopping")
        self.checkout = page.get_by_role("button", name="checkout")

    def verify_item_in_cart(self, item_name: str):
        expect(self.item_name).to_be_visible()

    def go_to_checkout(self) -> CheckoutPage:
        """Clicks the checkout buttons and returns the CheckoutPage object if successful.
        """
        self.checkout.click()

        return CheckoutPage(self.page)  # Return the new Page Object
