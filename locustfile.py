from locust import HttpUser, task, between
import random


class MyUser(HttpUser):
    """
    This is the user class that will be simulated by Locust.
    It inherits from HttpUser, which means it will make HTTP requests.
    """

    # The 'host' attribute is the base URL for the API you are testing.
    # Requests will be made relative to this URL.
    host = "https://jsonplaceholder.typicode.com"

    # 'wait_time' defines how long a user waits between executing tasks.
    # 'between(1, 2)' means each simulated user will wait randomly
    # between 1 and 2 seconds after completing a task before starting a new one.
    wait_time = between(1, 2)

    @task(weight=3)
    def get_single_post(self):
        """
        This method defines a user task: making a GET request to /posts/1.
        The @task decorator marks this method as a task that Locust users will execute.
        'self.client' is a requests.Session object, allowing you to make HTTP requests.
        """
        self.client.get("/posts/1", name="/posts/[id]")  # 'name' groups requests in stats

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
        We provide a JSON payload using the 'json' parameter.
        """
        post_payload = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        # Use self.client.post() and pass the JSON data using the 'json' argument
        self.client.post("/posts", json=post_payload, name="/posts")

    @task
    def get_random_post(self):
        post_id = random.randint(1, 100)  # Assuming 100 posts exist
        self.client.get(f"/posts/{post_id}", name="/posts/[id]")

    @task
    def create_dynamic_post(self):
        dynamic_title = f"Post by User {random.randint(1, 10)}"
        dynamic_body = f"Content at {self.environment.stats.num_requests}"  # Access environment for global stats
        post_payload = {
            "title": dynamic_title,
            "body": dynamic_body,
            "userId": random.randint(1, 10)
        }
        self.client.post("/posts", json=post_payload, name="/posts")
