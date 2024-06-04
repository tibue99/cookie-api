class CookieError(Exception):
    pass


class NotFound(CookieError):
    pass


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__("Could not find the user ID.")


class GuildNotFound(NotFound):
    def __init__(self):
        super().__init__("Could not find the guild ID.")


class NotOwner(CookieError):
    def __init__(self):
        super().__init__("The API key owner is not a member of the guild.")
