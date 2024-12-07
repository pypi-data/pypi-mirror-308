class ResponseError(Exception):
    """Raised when an API response is empty or has an unexpected format"""

    def __init__(self, message) -> None:
        self.message = "Invalid response from Flowery API: " + message


class InternalServerError(Exception):
    """Raised when the API returns a 5xx status code"""

    def __init__(self, message) -> None:
        self.message = message


class ClientError(Exception):
    """Raised when the API returns a 4xx status code"""

    def __init__(self, message) -> None:
        self.message = message


class TooManyRequests(Exception):
    """Raised when the API returns a 429 status code"""

    def __init__(self, message) -> None:
        self.message = message


class RetryLimitExceeded(Exception):
    """Raised when the retry limit is exceeded"""

    def __init__(self, message) -> None:
        self.message = message
