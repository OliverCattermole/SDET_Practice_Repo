import my_app
import requests  # Just for type-hinting/clarity in the test, not the patch target.
import datetime  # Need to import datetime here for patching its method


def test_fetch_post_title_mocked_confirmed(mocker):
    """
    Tests fetch_post_title by mocking requests.get with a unique return value.
    If this test passes and assert works on the unique value, the mock is confirmed.
    """
    print("\n--- Running Confirmation Mock Test ---")

    # Setup mock response with a unique title to avoid false positives
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "userId": 9999,  # Some unique ID
        "id": 9999,      # Some unique ID
        "title": "THIS IS A MOCKED TITLE - UNIQUE STRING",
        "body": "This is content from the mock."
    }
    mock_response.raise_for_status.return_value = None  # Ensure it behaves like a successful call

    # Patch 'requests.get' in the context of 'my_app'
    mocker.patch('my_app.requests.get', return_value=mock_response)

    # If the patch works, this call returns our unique title string above
    actual_title = my_app.fetch_post_title(1)

    # Confirm the function logic used the mocked data
    assert actual_title == "THIS IS A MOCKED TITLE - UNIQUE STRING"

    # Verify the API was called with the correct endpoint
    requests.get.assert_called_once_with("https://jsonplaceholder.typicode.com/posts/1")


def test_get_current_day_of_week_mocked(mocker):
    """
    Tests get_current_day_of_week by robustly mocking datetime.datetime.now().
    """
    print("\n--- Running Mock Time Test (Final Corrected) ---")

    # July 23, 2025 is a Wednesday
    fixed_datetime = datetime.datetime(2025, 7, 23, 10, 30, 0)

    # Patch the datetime class in my_app, so it uses our mock instead of system time
    mock_datetime_class = mocker.patch('my_app.datetime.datetime')
    mock_datetime_class.now.return_value = fixed_datetime

    day_of_week = my_app.get_current_day_of_week()

    # Assert the result based on our mocked time
    assert day_of_week == "Wednesday"
    # Assert that the mock's 'now' method was called
    mock_datetime_class.now.assert_called_once()
