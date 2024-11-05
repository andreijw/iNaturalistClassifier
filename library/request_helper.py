import logging
import threading
import requests

from requests import Session
from urllib3.util import Retry

logger = logging.getLogger(__name__)
thread_local = threading.local()


class RequestsHelper(Session):
    """Helper class to handle HTTP requests"""

    def __init__(self, max_retries: int = 3, timeout: int = 10):
        """Get a Session object, optionally with custom settings for caching and rate-limiting.

        Args:
            max_retries: Maximum number of times to retry a failed request
            timeout: The timeout for the request in seconds
        """

        self.timeout = timeout
        super().__init__()

        # Retry settings
        self.retries = Retry(total=max_retries)
        adapter = requests.adapters.HTTPAdapter(max_retries=self.retries)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

        # Default headers
        self.headers["Accept"] = "application/json"

    def send_request(
        url: str,
        method: str,
        return_type: str = "json",
        **kwargs,
    ) -> requests.Response:
        """Send an HTTP request

        Args:
            url: The URL to send the request to
            method: The HTTP method (GET, POST, PUT, DELETE, etc.)
            return_type: The type of response to return (json, text, etc.)
            params: The URL parameters to send with the request
            headers: The headers to send with the request
            data: The form data to send with the request
            json: The JSON data to send with the request

        Returns:
            The response object
        """
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"{method} request to {url} failed: {e}")
            return None

        if return_type == "json":
            return response.json()
        return response


def get_local_session(**kwargs) -> RequestsHelper:
    """Get a thread-local Session object with default settings. This will be reused across requests
    to take advantage of connection pooling and (optionally) caching. If used in a multi-threaded
    context (for example, a :py:class:`~concurrent.futures.ThreadPoolExecutor`), this will create
    and store a separate session object for each thread.

    Args:
        kwargs: Keyword arguments for :py:func:`.ClientSession`
    """
    if not hasattr(thread_local, "session"):
        thread_local.session = RequestsHelper(**kwargs)
    return thread_local.session
