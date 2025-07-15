# test_api_example.py
import pytest
import requests
BASE_URL = "https://jsonplaceholder.typicode.com"  # A public API for mock data

def test_get_all_posts():
    """
    Tests retrieving a list of all posts.
    Expected: Status code 200, and a list (JSON array) of posts.
    """
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list) # Ensure it's a list
    assert len(response.json()) > 0 # Ensure it's not empty
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
    assert response.status_code == 201 # 201 Created
    response_json = response.json()
    assert response_json["title"] == new_post_data["title"]
    assert response_json["body"] == new_post_data["body"]
    assert "id" in response_json # New post should have an ID
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
    post_id = 1 # We're deleting a mock post, so it won't actually disappear from the service
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    print(f"DELETE post (ID {post_id}) successful.")

def test_get_non_existent_post():
    """
    Tests retrieving a non-existent post.
    Expected: Status code 404 (Not Found).
    """
    post_id = 999999 # A very high ID to ensure it doesn't exist
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404
    print(f"GET non-existent post (ID {post_id}) returned 404 as expected.")