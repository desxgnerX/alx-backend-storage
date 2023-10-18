#!/usr/bin/env python3
""" Redis Module """

# Import required modules
from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis connection
redis_ = redis.Redis()


# Decorator to count requests made to the function
def count_requests(method: Callable) -> Callable:
    """ Decorator for counting the number of requests to a URL.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """ Wrapper function for the decorator.

        Args:
            url (str): The URL for which the request is made.

        Returns:
            str: The HTML content of the URL.
        """
        # Increment request count in Redis
        redis_.incr(f"count:{url}")

        # Check if cached HTML content is available
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # Make a request to the URL and cache the HTML content
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)  # Cache for 10 seconds
        return html

    return wrapper


# Function to obtain the HTML content of a URL
@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a URL.

    Args:
        url (str): The URL for which to obtain the HTML contentself.

    Returns:
        str: The HTML content of the URL.
    """
    req = requests.get(url)
    return req.text
