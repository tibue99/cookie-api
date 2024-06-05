import os
from datetime import date, datetime
from typing import overload

import aiohttp
from dotenv import load_dotenv

from .errors import GuildNotFound, InvalidAPIKey, NoGuildAccess, NotFound, UserNotFound
from .models import GuildActivity, MemberActivity, MemberStats, UserStats

DEFAULT_DAYS = 14


def _stats_dict(data: dict[str, int]) -> dict[date, int]:
    return {datetime.strptime(d, "%Y-%m-%d").date(): count for d, count in data.items()}


class CookieAPI:
    """A class to interact with the Cookie Bot API.

    Parameters
    ----------
    api_key:
        The API key to use. If no key is provided, ``COOKIE_KEY`` is loaded from the environment.
    """

    def __init__(self, api_key: str | None = None):
        self._session: aiohttp.ClientSession | None = None

        if api_key is None:
            load_dotenv()
            api_key = os.getenv("COOKIE_KEY")
            if api_key is None:
                raise InvalidAPIKey(
                    "Please provide an API key or set the COOKIE_KEY environment variable."
                )

        self._header = {"key": api_key, "accept": "application/json"}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def _setup(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    @overload
    async def _get(self, endpoint: str) -> dict: ...

    @overload
    async def _get(self, endpoint: str, stream: bool) -> bytes: ...

    async def _get(self, endpoint: str, stream: bool = False):
        async with self._session.get(
            f"https://api.cookie-bot.xyz/v1/{endpoint}", headers=self._header
        ) as response:
            if response.status == 401:
                raise InvalidAPIKey()
            elif response.status == 403:
                raise NoGuildAccess()
            elif response.status == 404:
                response = await response.json()
                message = response.get("detail")
                if "user" in message.lower() or "member" in message.lower():
                    raise UserNotFound()
                elif "guild" in message.lower():
                    raise GuildNotFound()
                raise NotFound()

            if stream:
                return await response.read()

            return await response.json()

    async def get_member_count(self, guild_id: int, days: int = DEFAULT_DAYS) -> dict[date, int]:
        """Get the history of the guild member count for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        GuildNotFound:
            The guild was not found.
        """
        await self._setup()
        message_data = await self._get(f"member_count/{guild_id}?days={days}")

        return _stats_dict(message_data)

    async def get_user_stats(self, user_id: int) -> UserStats:
        """Get the user's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.

        Raises
        ------
        UserNotFound:
            The user was not found.
        """
        await self._setup()
        data = await self._get(f"stats/user/{user_id}")
        return UserStats(user_id, **data)

    async def get_member_stats(self, user_id: int, guild_id: int) -> MemberStats:
        """Get the member's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.
        guild_id:
            The guild's ID.

        Raises
        ------
        UserNotFound:
            The user was not found.
        """
        await self._setup()
        data = await self._get(f"stats/member/{user_id}/{guild_id}")
        return MemberStats(user_id, guild_id, **data)

    async def get_member_activity(
        self, user_id: int, guild_id: int, days: int = 14
    ) -> MemberActivity:
        """Get the member's activity for the provided number of days.

        Parameters
        ----------
        user_id:
            The user's ID.
        guild_id:
            The guild's ID.
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        UserNotFound:
            The user was not found.
        """
        await self._setup()
        data = await self._get(f"activity/member/{user_id}/{guild_id}?days={days}")
        msg_activity = _stats_dict(data.pop("msg_activity"))
        voice_activity = _stats_dict(data.pop("voice_activity"))
        return MemberActivity(days, user_id, guild_id, msg_activity, voice_activity, **data)

    async def get_guild_activity(self, guild_id: int, days: int = DEFAULT_DAYS) -> GuildActivity:
        """Get the guild's activity for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID.
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        GuildNotFound:
            The guild was not found.
        """
        await self._setup()
        data = await self._get(f"activity/guild/{guild_id}?days={days}")
        msg_activity = _stats_dict(data.pop("msg_activity"))
        voice_activity = _stats_dict(data.pop("voice_activity"))
        return GuildActivity(days, guild_id, msg_activity, voice_activity, **data)

    async def get_guild_image(self, guild_id: int, days: int = DEFAULT_DAYS) -> bytes:
        """Get the guild's activity image for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID.
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        GuildNotFound:
            The guild was not found.
        """
        await self._setup()
        return await self._get(f"activity/guild/{guild_id}/image?days={days}", stream=True)

    async def get_member_image(
        self, user_id: int, guild_id: int, days: int = DEFAULT_DAYS
    ) -> bytes:
        """Get the member's activity image for the provided number of days.

        Parameters
        ----------
        user_id:
            The user's ID.
        guild_id:
            The guild's ID.
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        UserNotFound:
            The user was not found.
        """
        await self._setup()
        return await self._get(
            f"activity/member/{user_id}/{guild_id}/image?days={days}", stream=True
        )
