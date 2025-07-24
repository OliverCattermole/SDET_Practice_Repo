# pages/inventory_page.py
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """
    Page Object for the inventory/products page after successful login.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.products_title: Locator = page.locator(".title")
        self.shopping_cart_icon: Locator = page.locator("#shopping_cart_container")
        # Add other locators and methods specific to the Inventory Page here
        # e.g., add_to_cart_button, product_item_names, sort_dropdown

    def is_products_title_visible(self) -> bool:
        """Checks if the 'Products' title is visible on the page."""
        return self.products_title.is_visible()

    def get_products_title_text(self) -> str:
        """Returns the text content of the 'Products' title."""
        expect(self.products_title).to_be_visible() # Ensure it's visible before getting text
        return self.products_title.text_content()

    # Add methods for actions on this page, e.g., add_item_to_cart, view_cart