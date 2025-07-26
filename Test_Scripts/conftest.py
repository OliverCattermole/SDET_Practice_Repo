# conftest.py
import pytest


@pytest.fixture
def setup_data():
    """
    A simple fixture that provides some data for tests.
    This runs *before* any test that requests it.
    """
    print("\n--- Setting up data for test ---")
    data = {"username": "testuser", "password": "password123"}
    yield data  # 'yield' hands over control to the test function
    print("--- Cleaning up data after test ---")  # This runs *after* the test
