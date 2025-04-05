from __future__ import annotations

import json
import os
from typing import overload

import httpx
from dotenv import load_dotenv

from .errors import CookieError, InvalidAPIKey, NoGuildAccess, NotFound, QuotaExceeded
from .models import GuildActivity, GuildStats, MemberActivity, MemberStats, UserStats

DEFAULT_DAYS = 14
BASE_URL = "https://api.cookieapp.me/v1/"


def _handle_error(response: httpx.Response):
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise CookieError(response)
    status, message = None, None
    if "detail" in data:
        status = data["detail"].get("status")
        message = data["detail"].get("message")

    if response.status_code == 401:
        if status == "quota_exceeded":
            raise QuotaExceeded(message)
        else:
            raise InvalidAPIKey(message)
    elif response.status_code == 403:
        raise NoGuildAccess()
    elif response.status_code == 404:
        raise NotFound(message)
    else:
        raise CookieError(response)


class AsyncCookieAPI:
    """A class to interact with the Cookie API.

    Parameters
    ----------
    api_key:
        The API key to use. If no key is provided, ``COOKIE_KEY`` is loaded from the environment.
    session:
        An existing aiohttp session to use.
    """

    def __init__(self, api_key: str | None = None, session: httpx.AsyncClient | None = None):
        self._session: httpx.AsyncClient | None = session

        if api_key is None:
            load_dotenv()
            api_key = os.getenv("COOKIE_KEY")
            if api_key is None:
                raise InvalidAPIKey(
                    "Please provide an API key or set the COOKIE_KEY environment variable."
                )

        self._header = {"key": api_key, "accept": "application/json"}

    async def __aenter__(self):
        await self._setup()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def _setup(self):
        if self._session is None:
            self._session = httpx.AsyncClient()

    async def close(self):
        """Close the aiohttp session. When using the async context manager,
        this is called automatically.
        """

        await self._session.aclose()

    @overload
    async def _get(self, endpoint: str) -> dict: ...

    @overload
    async def _get(self, endpoint: str, stream: bool) -> bytes: ...

    async def _get(self, endpoint: str, stream: bool = False):
        await self._setup()
        response = await self._session.get(BASE_URL + endpoint, headers=self._header)
        if response.status_code != 200:
            _handle_error(response)

        if stream:
            return await response.aread()

        return response.json()

    async def get_guild_stats(self, guild_id: int, days: int = DEFAULT_DAYS) -> GuildStats:
        """Get the history of the guild member count for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        NoGuildAccess:
            You don't have access to that guild.
        """
        data = await self._get(f"stats/guild/{guild_id}?days={days}")
        return GuildStats(**data)

    async def get_user_stats(self, user_id: int) -> UserStats:
        """Get the user's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.

        Raises
        ------
        NotFound:
            The user was not found.
        """
        data = await self._get(f"stats/user/{user_id}")
        return UserStats(**data)

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
        NotFound:
            The user was not found.
        """
        data = await self._get(f"stats/member/{user_id}/{guild_id}")
        return MemberStats(**data)

    async def get_member_activity(
        self, user_id: int, guild_id: int, days: int = DEFAULT_DAYS
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
        NotFound:
            The user was not found.
        """
        data = await self._get(f"activity/member/{user_id}/{guild_id}?days={days}")
        return MemberActivity(**data)

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
        NoGuildAccess:
            You don't have access to that guild.
        """
        data = await self._get(f"activity/guild/{guild_id}?days={days}")
        return GuildActivity(**data)

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
        NoGuildAccess:
            You don't have access to that guild.
        """
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
        NotFound:
            The user was not found.
        """
        return await self._get(
            f"activity/member/{user_id}/{guild_id}/image?days={days}", stream=True
        )


class CookieAPI:
    """A class to interact with the Cookie API.

    Parameters
    ----------
    api_key:
        The API key to use. If no key is provided, ``COOKIE_KEY`` is loaded from the environment.
    httpx_client:
        An existing httpx client to use.
    """

    def __init__(self, api_key: str | None = None, httpx_client: httpx.Client | None = None):
        self._httpx_client: httpx.Client | None = httpx_client

        if httpx_client is None:
            self._httpx_client = httpx.Client()
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("COOKIE_KEY")
            if api_key is None:
                raise InvalidAPIKey(
                    "Please provide an API key or set the COOKIE_KEY environment variable."
                )

        self._header = {"key": api_key, "accept": "application/json"}

    @overload
    def _get(self, endpoint: str) -> dict: ...

    @overload
    def _get(self, endpoint: str, stream: bool) -> bytes: ...

    def _get(self, endpoint: str, stream: bool = False):
        response = self._httpx_client.get(BASE_URL + endpoint, headers=self._header)
        if response.status_code != 200:
            _handle_error(response)

        if stream:
            return response.read()

        return response.json()

    def get_guild_stats(self, guild_id: int, days: int = DEFAULT_DAYS) -> GuildStats:
        """Get the history of the guild member count for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        NoGuildAccess:
            You don't have access to that guild.
        """
        data = self._get(f"stats/guild/{guild_id}?days={days}")
        return GuildStats(**data)

    def get_user_stats(self, user_id: int) -> UserStats:
        """Get the user's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.

        Raises
        ------
        NotFound:
            The user was not found.
        """
        data = self._get(f"stats/user/{user_id}")
        return UserStats(**data)

    def get_member_stats(self, user_id: int, guild_id: int) -> MemberStats:
        """Get the member's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.
        guild_id:
            The guild's ID.

        Raises
        ------
        NotFound:
            The user was not found.
        """
        data = self._get(f"stats/member/{user_id}/{guild_id}")
        return MemberStats(**data)

    def get_member_activity(
        self, user_id: int, guild_id: int, days: int = DEFAULT_DAYS
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
        NotFound:
            The user was not found.
        """
        data = self._get(f"activity/member/{user_id}/{guild_id}?days={days}")
        return MemberActivity(**data)

    def get_guild_activity(self, guild_id: int, days: int = DEFAULT_DAYS) -> GuildActivity:
        """Get the guild's activity for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID.
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        NoGuildAccess:
            You don't have access to that guild.
        """
        data = self._get(f"activity/guild/{guild_id}?days={days}")
        return GuildActivity(**data)

    def get_guild_image(self, guild_id: int, days: int = DEFAULT_DAYS) -> bytes:
        """Get the guild's activity image for the provided number of days.

        Parameters
        ----------
        guild_id:
            The guild's ID.
        days:
            The number of days. Defaults to ``14``.

        Raises
        ------
        NoGuildAccess:
            You don't have access to that guild.
        """
        return self._get(f"activity/guild/{guild_id}/image?days={days}", stream=True)

    def get_member_image(self, user_id: int, guild_id: int, days: int = DEFAULT_DAYS) -> bytes:
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
        NotFound:
            The user was not found.
        """
        return self._get(f"activity/member/{user_id}/{guild_id}/image?days={days}", stream=True)
