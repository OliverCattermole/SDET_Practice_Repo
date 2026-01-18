from locust import HttpUser, task, between
import random


class MyUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"

    # Simulates "think time" between actions
    wait_time = between(1, 2)

    @task(weight=3)
    def get_single_post(self):
        # Using 'name' param so Locust groups all individual post IDs into one stat line
        self.client.get("/posts/1", name="/posts/[id]")

    @task(weight=2)
    def get_all_users(self):
        """
        Another task: making a GET request to /users.
        """
        self.client.get("/users", name="/users")

    @task(weight=1)
    def create_new_post(self):
        """
        This task simulates creating a new post using a POST request.
        """
        post_payload = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        self.client.post("/posts", json=post_payload, name="/posts")

    @task
    def get_random_post(self):
        post_id = random.randint(1, 100)  # Assuming 100 posts exist
        self.client.get(f"/posts/{post_id}", name="/posts/[id]")

    @task
    def create_dynamic_post(self):
        # Using global request count in the body to ensure unique payloads
        dynamic_title = f"Post by User {random.randint(1, 10)}"
        dynamic_body = f"Content at {self.environment.stats.num_requests}"
        post_payload = {
            "title": dynamic_title,
            "body": dynamic_body,
            "userId": random.randint(1, 10)
        }
        self.client.post("/posts", json=post_payload, name="/posts")
