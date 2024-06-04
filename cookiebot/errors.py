class CookieError(Exception):
    pass


class NotFound(CookieError):
    pass


class UserNotFound(NotFound):
    pass


class GuildNotFound(NotFound):
    pass


class NotOwner(CookieError):
    pass
