# test_api_example.py
import pytest
import requests
import os  # Import the os module to access environment variables
import json
from jsonschema import validate, ValidationError
# Read BASE_URL from an environment variable, with a fallback for local execution
BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")  # A public API for mock data
# If API_BASE_URL is not set, it will default to jsonplaceholder.typicode.com


def test_get_all_posts():
    """
    Tests retrieving a list of all posts.
    Expected: Status code 200, and a list (JSON array) of posts.
    """
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure it's a list
    assert len(response.json()) > 0  # Ensure it's not empty
    print(f"\nGET all posts successful. Found {len(response.json())} posts.")


def test_get_single_post():
    """
    Tests retrieving a single post by ID.
    Expected: Status code 200, and specific post ID.
    """
    post_id = 1
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["id"] == post_id
    assert "title" in post_data
    assert "body" in post_data
    print(f"GET single post (ID {post_id}) successful. Title: {post_data['title'][:30]}...")

# A couple of data Driven API tests


@pytest.mark.parametrize("post_id, expected_title_contains", [
    (1, "sunt aut facere"),  # Valid post 1
    (10, "optio molestias id quia eum"),  # Valid post 10
    (100, "at nam consequatur"),  # Valid post 100
    (999999, None)  # Non-existent post (we'll adapt the test for this)
])
def test_get_single_post_data_driven(post_id, expected_title_contains):
    """
    Tests retrieving a single post by ID using parametrization.
    """
    response = requests.get(f"{BASE_URL}/posts/{post_id}")

    if expected_title_contains is not None:
        # For valid posts
        assert response.status_code == 200
        post_data = response.json()
        assert post_data["id"] == post_id
        assert expected_title_contains in post_data["title"]
        print(f"GET post ID {post_id} successful. Title contains: '{expected_title_contains}'.")
    else:
        # For non-existent posts
        assert response.status_code == 404
        print(f"GET non-existent post ID {post_id} returned 404 as expected.")


@pytest.mark.parametrize("test_case_name, payload, expected_status_code", [
    ("Valid Post Creation", {"title": "Test Title 1", "body": "Test Body 1", "userId": 1}, 201),
    ("Another Valid Post", {"title": "Another Title", "body": "Another Body", "userId": 2}, 201),
    ("Post with Missing Body", {"title": "No Body Post", "userId": 3}, 201),  # JSONPlaceholder often still accepts this
    ("Post with Extra Field", {"title": "Extra Field", "body": "Data", "extra_field": "value", "userId": 4}, 201)
    # JSONPlaceholder is very forgiving; a real API would likely return 400 for invalid payloads
])
def test_create_post_data_driven(test_case_name, payload, expected_status_code):
    """
    Tests creating posts with different payloads using parametrization.
    """
    print(f"\n--- Running Test Case: {test_case_name} ---")
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == expected_status_code

    if expected_status_code == 201:
        response_json = response.json()
        # Assert that the received data matches the sent payload (or a subset)
        for key, value in payload.items():
            assert response_json.get(key) == value
        assert "id" in response_json  # Ensure an ID was assigned
        print(f"Post created successfully with ID: {response_json.get('id')}. Title: {response_json.get('title')}.")
    else:
        print(f"Post creation failed as expected with status code: {response.status_code}.")


def test_create_new_post():
    """
    Tests creating a new post using POST request.
    Expected: Status code 201 (Created), and the response contains the new post's ID.
    """
    new_post_data = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post_data)
    assert response.status_code == 201  # 201 Created
    response_json = response.json()
    assert response_json["title"] == new_post_data["title"]
    assert response_json["body"] == new_post_data["body"]
    assert "id" in response_json  # New post should have an ID
    print(f"POST new post successful. New ID: {response_json['id']}")


def test_update_existing_post():
    """
    Tests updating an existing post using PUT request.
    Expected: Status code 200 (OK), and the response reflects the updated data.
    """
    post_id = 1
    updated_data = {
        "id": post_id,
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["title"] == updated_data["title"]
    assert response_json["body"] == updated_data["body"]
    assert response_json["id"] == post_id
    print(f"PUT update post (ID {post_id}) successful. New Title: {response_json['title']}")


def test_delete_post():
    """
    Tests deleting a post using DELETE request.
    Expected: Status code 200 (OK), and typically an empty response or confirmation.
    """
    post_id = 1  # We're deleting a mock post, so it won't actually disappear from the service
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    print(f"DELETE post (ID {post_id}) successful.")


def test_get_non_existent_post():
    """
    Tests retrieving a non-existent post.
    Expected: Status code 404 (Not Found).
    """
    post_id = 999999  # A very high ID to ensure it doesn't exist
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404
    print(f"GET non-existent post (ID {post_id}) returned 404 as expected.")

# JSON Schema related tests


def load_json_schema(filename):
    """Loads a JSON schema from the 'schemas' directory."""
    filepath = f"Test_Scripts/schemas/{filename}"  # Adjust path if your schemas folder is elsewhere
    with open(filepath, 'r') as file:
        return json.load(file)


POST_SCHEMA = load_json_schema("post_schema.json")


def test_get_single_post_schema_validation():
    """
    Tests retrieving a single valid post and validates its schema.
    """
    post_id = 1
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    post_data = response.json()

    try:
        validate(instance=post_data, schema=POST_SCHEMA)
        print(f"\nResponse for post ID {post_id} successfully validated against schema.")
    except ValidationError as e:
        pytest.fail(f"Schema validation failed for post ID {post_id}:\n{e.message}\nPath: {e.path}\nValidator: {e.validator}\nValidator Value: {e.validator_value}")

# Optional: Test with an invalid schema (if you can simulate one)
# This example will fail on purpose to show validation errors


def test_invalid_post_schema_validation_example():
    """
    Demonstrates schema validation failure with an invalid response structure.
    This test is expected to fail.
    """
    invalid_data = {
        "userId": "1",  # Should be integer, not string
        "id": 1,
        "title": "A valid title",
        "body": "A valid body",
        "extraField": "unexpected value"  # additionalProperties: false should catch this
    }
    # For demonstration, we'll try to validate this incorrect data against our schema
    # In a real test, you'd be getting this from an API call that returned bad data

    try:
        validate(instance=invalid_data, schema=POST_SCHEMA)
        pytest.fail("Schema validation unexpectedly passed for invalid data!")
    except ValidationError as e:
        print(f"\nSuccessfully caught expected schema validation error:\n{e.message}\nPath: {e.path}\nValidator: {e.validator}\nValidator Value: {e.validator_value}")
        # Assert specific aspects of the error if needed
        assert "is not of type 'integer'" in e.message or "'extraField' was unexpected" in e.message
        assert (e.path and e.path[0] == "userId") or e.validator == "additionalProperties"
        print("Expected schema validation error caught successfully.")
