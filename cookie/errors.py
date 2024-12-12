class CookieError(Exception):
    """Base exception class for all Cookie exceptions."""

    pass


class InvalidAPIKey(CookieError):
    """Raised when an invalid API key is provided or if no key was found
    in the environment variables.
    """

    def __init__(self, msg: str | None = None):
        super().__init__(msg or "Please provide a valid API key.")


class QuotaExceeded(CookieError):
    """Raised when the monthly usage limit is exceeded."""

    def __init__(self, msg: str | None = None):
        super().__init__(msg or "You have exceeded the monthly usage limit.")


class NotFound(CookieError):
    """Raised when an object is not found."""

    pass


class NoGuildAccess(CookieError):
    """Raised when you do not have access to a guild."""

    def __init__(self):
        super().__init__("You are not a member of this guild.")
