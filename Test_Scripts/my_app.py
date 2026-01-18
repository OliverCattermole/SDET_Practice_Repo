import requests
import datetime


def fetch_post_title(post_id):
    """
    Fetches a post from JSONPlaceholder using requests.get
    and returns its title.
    """
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    print(f"DEBUG: Making actual API call to {url}")  # For demonstration
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (e.g., 4xx or 5xx)
    return response.json().get('title')


def get_current_day_of_week():
    """Returns the current day of the week as a string (e.g., 'Monday')."""
    now = datetime.datetime.now()
    print(f"DEBUG: Current datetime.datetime.now() is {now}")  # For demo
    return now.strftime("%A")  # %A means full weekday name
