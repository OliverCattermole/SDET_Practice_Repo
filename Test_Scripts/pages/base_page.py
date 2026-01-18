from playwright.sync_api import Page, expect


class BasePage:
    """
       A base class for all Page Objects, providing common functionalities
       like navigation, waiting, and common locators (e.g., for headers/footers).
       """

    def __init__(self, page: Page):
        self.page = page
        # Example of a common locator if all pages had one:
        # self.header_title = page.locator("h1.header")
        self.page_title = page.locator(".title")  # Locator for success page title

    def goto(self, url: str):
        """Navigates to a specific URL."""
        self.page.goto(url)
        # Generic example - wait until network is idle before proceeding
        self.page.wait_for_load_state("networkidle")

    def get_page_title(self) -> str:
        """Returns the current page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Returns the current URL."""
        return self.page.url
