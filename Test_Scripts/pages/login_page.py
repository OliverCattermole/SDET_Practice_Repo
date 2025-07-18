from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators (using Playwright's recommended locators where possible)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test=\"error\"]")
        self.inventory_page_title = page.locator(".title")  # Locator for success page title

    def navigate(self):
        """Navigates to the login page."""
        self.page.goto("https://www.saucedemo.com/")
        # Ensure the login button is visible before attempting interaction
        expect(self.login_button).to_be_visible()

    def login(self, username, password):
        """Performs a login action with given credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message_text(self):
        """Returns the text of the error message."""
        # Explicitly wait for the error message to be visible and stable before getting its text
        expect(self.error_message).to_be_visible()
        return self.error_message.text_content()

    def is_error_message_visible(self):
        """Checks if the error message element is visible."""
        return self.error_message.is_visible()

    def login_and_expect_success(self, username, password):
        self.login(username, password)
        # Assert that URL changes AND a specific element on the next page is visible
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(self.inventory_page_title).to_have_text(
            "Products")  # Explicitly wait for the title element to be correct
        # No return needed, just assertions for successful login flow