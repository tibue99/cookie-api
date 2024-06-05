class CookieError(Exception):
    pass


class InvalidAPIKey(CookieError):
    def __init__(self, msg: str | None = None):
        super().__init__(msg or "Invalid API key.")


class NotFound(CookieError):
    pass


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__("Could not find the user ID.")


class GuildNotFound(NotFound):
    def __init__(self):
        super().__init__("Could not find the guild ID.")


class NoGuildAccess(CookieError):
    def __init__(self):
        super().__init__("You are not a member of this guild.")
