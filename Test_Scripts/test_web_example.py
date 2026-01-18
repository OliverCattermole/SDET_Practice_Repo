import pytest
from playwright.sync_api import Page, expect

# The 'page' fixture is automatically provided by pytest-playwright
# It represents a single browser tab/page.

from pages.login_page import LoginPage


def test_example_page_title(page: Page):
    """
    Tests that the Playwright doc page has the correct title.
    """
    page.goto("https://playwright.dev/python/docs/intro")
    expect(page).to_have_title("Installation | Playwright Python")
    print(f"\nPage title is: {page.title()}")
    page.screenshot(path="intro_page.png")
    print("Screenshot saved to intro_page.png")


def test_search_on_google(page: Page):
    """
    Navigates to Google, searches for a term, and verifies results.
    """
    page.goto("https://www.google.com")

    # Handle the cookie consent pop-up
    page.get_by_role("button", name="Accept all").click()

    # Preferring title locator here over combobox for stability
    search_box = page.get_by_title("Search")
    search_box.fill("Playwright testing Python")  # Type text into the field
    search_box.press("Enter")  # Simulate pressing Enter

    page.screenshot(path="Google Search_results.png")
    print("Screenshot saved to Google Search_results.png")


def test_invalid_login_scenario(page: Page):
    """
    Simulates an invalid login and asserts an error message.
    """
    page.goto("https://www.saucedemo.com/")

    # # Locate and fill username field
    # page.locator("#user-name").fill("invalid_user")
    # # Locate and fill password field
    # page.locator("[data-test=\"password\"]").fill("wrong_password")

    # Switching to ID locators for better reliability
    page.locator('id=user-name').fill("invalid_user")
    page.locator("id=password").fill("wrong_password")
    page.locator("#login-button").click()

    expect(page.locator("[data-test=\"error\"]")).to_have_text("Epic sadface: Username and password do not match any user in this service")
    print("\nInvalid login error message verified.")
    page.screenshot(path="invalid_login_error.png")


def test_invalid_login_scenario_with_page_object(page: Page):
    """
    Simulates an invalid login and asserts an error message using POM.
    """
    login_page = LoginPage(page)

    login_page.navigate()  # Use the Page Object's navigation method
    login_page.login("invalid_user", "wrong_password")  # Use the Page Object's login method

    expect(login_page.error_message).to_have_text("Epic sadface: Username and password do not match any user in this service")
    print("\nInvalid login error message verified.")
    page.screenshot(path="invalid_login_error_page_object.png")

# Robust method


def test_successful_login_scenario(page: Page):
    """
    Simulates a successful login and asserts navigation using POM with explicit waits.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login_and_expect_success("standard_user", "secret_sauce")  # Uses robust method
    print("\nSuccessful login verified using robust Page Object Model.")
    page.screenshot(path="successful_login_pom.png")


# Basic Network Interception

def test_mock_api_response(page: Page):
    """
    Mocks an API response to test a UI component's behaviour without needing a real backend
    """
    mock_url = "http://localhost:8000/api/data"

    # Fulfill the request locally, so we don't need a real backend
    page.route(mock_url, lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"message": "Data successfully mocked!"}'
    ))

    # Trigger a fetch to the mocked endpoint via injected JS
    page.goto(f"data:text/html,<script>"
              f"fetch('{mock_url}')"
              f".then(r=>r.json())"
              f".then(j=>document.body.textContent=j.message)"
              f".catch(e=>document.body.textContent='Error: ' + e.message)"  # Added error handling for clarity
              f"</script>")

    # Assert that the mocked data is displayed on the page
    expect(page.locator("body")).to_have_text("Data successfully mocked!")
    print("\nAPI response successfully mocked and verified.")
    page.screenshot(path="mocked_api_response.png")


def test_block_image_request(page: Page):
    """
    Blocks requests for images to speed up page loading or test resilience.
    """
    page.route("**/*.{png,jpg,jpeg,gif,webp}", lambda route: route.abort())

    page.goto("https://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day")

    # Verify that the page still loads and has content (though images will be missing)
    expect(page.locator("h1")).to_have_text("Wikipedia:Picture of the day")
    print("\nImage requests blocked. Page loaded without images.")
    page.screenshot(path="blocked_images_wikipedia.png")

# def test_saucedemo_login_page_visual(page: Page, image_regression):
#     """
#     Tests the visual appearance of the Saucedemo login page using image_regression.
#     """
#     page.goto("https://www.saucedemo.com/")
#     page.wait_for_selector("#login-button", state="visible")
#
#     page.goto("https://www.google.com")
#
#     # Get screenshot bytes from Playwright
#     screenshot_bytes = page.screenshot()
#
#     # Call the image_regression fixture with the screenshot bytes
#     # The first argument is the image content. The second is the filename.
#     # The threshold can be set directly in the call or using a fixture.
#     assert image_regression(screenshot_bytes, threshold=0.5) # Using 0.5 as a default threshold, adjust as needed
#
#     print("\nSaucedemo login page visual test executed.")


@pytest.mark.parametrize("username, password, expected_outcome", [
    ("standard_user", "secret_sauce", "success"),
    ("locked_out_user", "secret_sauce", "error"),
    ("invalid_user", "wrong_password", "error")
])
def test_login_scenarios(page: Page, username, password, expected_outcome):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    if expected_outcome == "success":
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    else:
        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text(
            "Epic sadface")

    print(f"Login for user '{username}' tested with expected outcome: {expected_outcome}")
