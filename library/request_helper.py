import logging
import threading
import requests

from urllib.parse import urlencode, quote
from requests import Session, Request, PreparedRequest
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
        self,
        method: str,
        url: str,
        params: dict = None,
        headers: dict = None,
        data: dict = None,
        json: dict = None,
        return_type: str = "json",
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
            return_type: The type of response to return (json, text, etc.)

        Returns:
            The response object
        """
        try:
            if params:
                encoded_params = urlencode(params, quote_via=quote)
                url = f"{url}?{encoded_params}"

            request = Request(
                method=method,
                url=url,
                headers=headers or self.headers,
                data=data,
                json=json,
            )
            prepared_request = self.prepare_request(request)
            response = self.send(prepared_request, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"{method} request to {url} failed: {e}")
            return None

        breakpoint()
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
