# pages/checkout_page.py
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """
    Page Object for the checkout page.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators (using Playwright's recommended locators where possible)
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.cancel_button = page.get_by_role("button", name="cancel")
        self.continue_button = page.locator("[data-test=\"continue\"]")

    def fill_user_info(self, first_name, last_name, postal_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_checkout_two(self):
        self.continue_button.click()

