import my_app
import requests  # This import is just for type-hinting/clarity in the test, not the patch target.
import datetime  # Need to import datetime here for patching its method


def test_fetch_post_title_mocked_confirmed(mocker):
    """
    Tests fetch_post_title by mocking requests.get with a unique return value.
    If this test passes and assert works on the unique value, the mock is confirmed.
    """
    print("\n--- Running Confirmation Mock Test ---")

    # 1. Define a mock response object with a UNIQUE title
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "userId": 9999,  # Some unique ID
        "id": 9999,      # Some unique ID
        "title": "THIS IS A MOCKED TITLE - UNIQUE STRING",  # <= VERY UNIQUE!
        "body": "This is content from the mock."
    }
    mock_response.raise_for_status.return_value = None  # Ensure it behaves like a successful call

    # 2. Patch 'requests.get' in the context of 'my_app'
    mocker.patch('my_app.requests.get', return_value=mock_response)

    # 3. Call the function we are actually testing
    # This call will now use our patched requests.get, not the real one.
    actual_title = my_app.fetch_post_title(1)

    # 4. Assert on the result of our function's logic.
    # This assertion will ONLY pass if the mock was hit and returned our unique title.
    assert actual_title == "THIS IS A MOCKED TITLE - UNIQUE STRING"

    # 5. Assert on the mock itself (optional, but good practice)
    requests.get.assert_called_once_with("https://jsonplaceholder.typicode.com/posts/1")


def test_get_current_day_of_week_mocked(mocker):
    """
    Tests get_current_day_of_week by robustly mocking datetime.datetime.now().
    """
    print("\n--- Running Mock Time Test (Final Corrected) ---")

    # 1. Define the specific datetime object we want datetime.datetime.now() to return.
    fixed_datetime = datetime.datetime(2025, 7, 23, 10, 30, 0)  # This is a Wednesday

    # 2. Patch the 'datetime.datetime' CLASS itself.
    #    This replaces the entire 'datetime.datetime' class within 'my_app' with a Mock.
    mock_datetime_class = mocker.patch('my_app.datetime.datetime')

    # 3. Now, tell the 'now' method of our MOCKED class what to return.
    #    When my_app calls datetime.datetime.now(), it's now calling now() on this mock.
    mock_datetime_class.now.return_value = fixed_datetime

    # 4. Call the function under test
    day_of_week = my_app.get_current_day_of_week()

    # 5. Assert the result based on our mocked time
    assert day_of_week == "Wednesday"

    # 6. Assert that the mock's 'now' method was called (good practice)
    mock_datetime_class.now.assert_called_once()
