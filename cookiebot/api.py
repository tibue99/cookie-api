from datetime import date, datetime

import aiohttp

from .errors import GuildNotFound, InvalidAPIKey, NotFound, NotOwner, UserNotFound
from .models import GuildActivity, MemberActivity, MemberStats, UserStats


class CookieAPI:
    def __init__(self, api_key: str):
        self._session: aiohttp.ClientSession | None = None
        self._header = {"key": api_key, "accept": "application/json"}

    async def setup(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    async def _get(self, endpoint: str) -> dict:
        async with self._session.get(
            f"https://api.cookie-bot.xyz/premium/v1/{endpoint}", headers=self._header
        ) as response:
            if response.status == 401:
                raise InvalidAPIKey()
            elif response.status == 403:
                print(await response.json())
                raise NotOwner()
            elif response.status == 404:
                response = await response.json()
                message = response.get("detail")
                if "user" in message.lower():
                    raise UserNotFound()
                elif "guild" in message.lower():
                    raise GuildNotFound()
                raise NotFound()

            return await response.json()

    async def get_member_count(self, guild_id: int, days: int = 14) -> dict[date, int]:
        """Indicates the number of members on the guild on the respective day.

        Parameters
        ----------
        guild_id:
            The guild id from the guild.
        days:
            The number of days.
        """
        await self.setup()
        message_data = await self._get(f"member_count/{guild_id}?days={days}")

        return {datetime.strptime(d, "%Y-%m-%d").date(): count for d, count in message_data.items()}

    async def get_user_stats(self, user_id: int) -> UserStats:
        """Stats for a user.

        Parameters
        ----------
        user_id:
            The user's ID.
        """
        await self.setup()
        data = await self._get(f"stats/user/{user_id}")
        return UserStats(user_id, **data)

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
        data = await self._get(f"stats/member/{user_id}/{guild_id}")
        return MemberStats(user_id, guild_id, **data)

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
        data = await self._get(f"activity/member/{user_id}/{guild_id}?days={days}")
        return MemberActivity(days, user_id, guild_id, **data)

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
        data = await self._get(f"activity/guild/{guild_id}?days={days}")
        return GuildActivity(days, **data)
