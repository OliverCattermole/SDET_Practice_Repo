# test_example.py
import pytest


@pytest.mark.parametrize("num1, num2, expected_sum", [
    (1, 2, 3),
    (-1, 5, 4),
    (0, 0, 0),
    (100, -50, 50)
])
def test_add_function_parametrized(num1, num2, expected_sum):
    """
    Tests the 'add' function with multiple sets of inputs using parametrization
    """
    print(f"\nTesting add({num1}, {num2}) -> Expected: {expected_sum}")
    result = add(num1, num2)  # Using the 'add' function defined previously
    assert result == expected_sum


# You can even parametrize a fixture! (More advanced, but good to see)
@pytest.fixture(params=[
    ("user_a", "pass_a"),
    ("user_b", "pass_b")
])
def parameterized_user(request):
    """ A fixture that provides different user credentials"""
    username, password = request.param
    print(f"\n--- Setting up parameterized user: {username} ---")
    yield {"username": username, "password": password}
    print(f"--- Cleaning up parameterized user: {username} ---")


def test_login_with_different_users(parameterized_user):
    """
    Tests login with different users provided by a parameterized fixture.
    """
    print(f"Attempting login for user: {parameterized_user['username']}")
    assert parameterized_user['password'] == "pass_a" or parameterized_user['password'] == "pass_b"
    assert parameterized_user['username'].startswith("user_")
    print(f"Login successful for {parameterized_user['username']} (simulated).")


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def test_add_positive_numbers():
    """TEST adding two positive numbers."""
    assert add(2, 3) == 5


def test_add_negative_numbers():
    """TEST adding a positive and a negative number."""
    assert add(-1, 5) == 4


def test_subtract_numbers():
    """TEST basic subtraction."""
    assert subtract(10, 3) == 7


def test_multiply_numbers():
    """TEST basic multiplication."""
    assert multiply(4, 5) == 20


def test_failing_example():
    """This test is designed to fail to see Pytest's output."""
    assert add(1, 1) == 2  # This will fail


def test_login_with_fixture(setup_data):
    """
    Test a bsic login scenario using data from the fixture.
    'setup_data' is the name of the fixture function from conftest.py.
    Pytest automatically injects the 'data' dictionary into this argument.
    """
    print(f"\nAttempting login with username: {setup_data['username']}")
    # Simulate a login check
    assert setup_data["username"] == "testuser"
    assert setup_data["password"] == "password123"
    print("Login successful (simulated).")


def test_another_test_with_fixture(setup_data):
    """Another test demonstrating fixture reuse."""
    print(f"\nUsing some other data: {setup_data}")
    assert "username" in setup_data
    assert setup_data["password"] == "password123"
