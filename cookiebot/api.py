import aiohttp

from .errors import GuildNotFound, NotOwner, UserNotFound
from .models import GuildActivity, MemberActivity, MemberStats, UserStats

BASE_URL = "https://api.cookie-bot.xyz/premium"


class CookieAPI:
    def __init__(self, api_key: str):
        self._session: aiohttp.ClientSession | None = None
        self._header = {"key": api_key, "accept": "application/json"}

    async def setup(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    @staticmethod
    async def _check_error(status_code: int, errors: dict):
        for error_code in errors.keys():
            if status_code == error_code:
                error = errors[error_code]
                raise error()

    async def get_member_count(self, guild_id: int, days: int) -> dict:
        """Indicates the number of members on the guild on the respective day.

        Parameters
        ----------
        guild_id:
            The guild id from the guild.
        days:
            The number of days.
        """
        await self.setup()
        async with self._session.get(
            BASE_URL + f"/members/{guild_id}?days={days}", headers=self._header
        ) as response:
            await self._check_error(response.status, {401: NotOwner})
            return await response.json()

    async def get_user_stats(self, user_id: int) -> UserStats:
        """Stats for a user.

        Parameters
        ----------
        user_id:
            The user's ID.
        """
        await self.setup()
        async with self._session.get(
            BASE_URL + f"/stats/user/{user_id}", headers=self._header
        ) as response:
            await self._check_error(response.status, {404: UserNotFound})
            data = await response.json()
            return UserStats(user_id, **data)

    async def get_member_activity(
        self, user_id: int, guild_id: int, days: int = 14
    ) -> MemberActivity:
        """Return the user's activity stats for the last x days.

        Parameters
        ----------
        user_id:
            The user id from the user.
        guild_id:
            The guild id from the guild.
        days:
            The number of days.
        """
        await self.setup()
        async with self._session.get(
            BASE_URL + f"/stats/user/{user_id}/{guild_id}?days={days}", headers=self._header
        ) as response:
            await self._check_error(response.status, {404: UserNotFound, 401: GuildNotFound})
            data = await response.json()
            return MemberActivity(days, user_id, guild_id, **data)

    async def get_member_stats(self, user_id: int, guild_id: int) -> MemberStats:
        """Return the user's level stats.

        Parameters
        ----------
        user_id:
            The user id from the user.
        guild_id:
            The guild id from the guild.
        """
        await self.setup()
        async with self._session.get(
            BASE_URL + f"/stats/user/{user_id}/{guild_id}", headers=self._header
        ) as response:
            await self._check_error(response.status, {404: UserNotFound, 401: GuildNotFound})
            data = await response.json()
            return MemberStats(user_id, guild_id, **data)

    async def get_guild_activity(self, guild_id: int, days: int = 14) -> GuildActivity:
        """Guild stats for provided days.

        Parameters
        ----------
        guild_id:
            The guild id from the guild.
        days:
            The number of days.
            Defaults to ``14``.
        """
        await self.setup()
        async with self._session.get(
            BASE_URL + f"/stats/guild/{guild_id}?days={days}", headers=self._header
        ) as response:
            await self._check_error(response.status, {401: GuildNotFound})
            data = await response.json()
            return GuildActivity(days, **data)
