from playwright.sync_api import Page, expect
from pages.base_page import BasePage # Import the new BasePage
from pages.inventory_page import InventoryPage # Import the new InventoryPage

class LoginPage(BasePage):  # Inherit from BasePage
    def __init__(self, page: Page):
        super().__init__(page)  # Call the constructor of the parent class
        self.page = page
        # Locators (using Playwright's recommended locators where possible)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test=\"error\"]")
        #self.inventory_page_title = page.locator(".title")  # Locator for success page title

    def navigate(self):
        """Navigates to the login page using the BasePage's goto method."""
        self.goto("https://www.saucedemo.com/")  # Use the inherited goto method
        # Ensure the login button is visible before attempting interaction
        expect(self.login_button).to_be_visible()

    def login(self, username, password):
        """Performs a login action with given credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_successfully(self, username, password) -> InventoryPage:
        """Performs a login action and returns the InventoryPage object if successful.
        This method is designed for scenarios where a successful login is expected
        and you want to immediately interact with the next page.
        """
        self.login(username, password)
        # Use Playwright's expect to wait for the URL change or element presence,
        # ensuring the page loaded correctly before returning the new Page Object.
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        # The next assertion about the title (or any specific element) should
        # be done on the InventoryPage object itself, or directly in the test.
        # Here we verify the page navigated to the correct URL before returning.

        return InventoryPage(self.page)  # Return the new Page Object

    def get_error_message_text(self) -> str:
        """Returns the text of the error message."""
        # Explicitly wait for the error message to be visible and stable before getting its text
        expect(self.error_message).to_be_visible()
        return self.error_message.text_content()

    def is_error_message_visible(self) -> bool:
        """Checks if the error message element is visible."""
        return self.error_message.is_visible()

    def login_and_expect_success(self, username, password):
        self.login(username, password)
        # Assert that URL changes AND a specific element on the next page is visible
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(self.get_page_title).to_have_text("Products")
        #expect(self.inventory_page_title).to_have_text(
            #"Products")  # Explicitly wait for the title element to be correct
        # No return needed, just assertions for successful login flow