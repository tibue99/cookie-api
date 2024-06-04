import aiohttp

from .errors import GuildNotFound, NotOwner, UserNotFound
from .models import GuildActivity, MemberActivity, MemberStats, UserStats

BASE_URL = "https://api.cookie-bot.xyz/premium"
GUILD_NOT_FOUND_TEXT = "Could not find the guild ID."
USER_NOT_FOUND_TEXT = "Could not find the user ID."


class CookieAPI:
    def __init__(self, api_key: str):
        self._session: aiohttp.ClientSession | None = None
        self.api_key = api_key
        self._header = {"key": self.api_key, "accept": "application/json"}

    async def _check_session(self):
        if self._session is None:
            await self._setup()

    async def _setup(self):
        self._session = aiohttp.ClientSession()

    async def _close(self):
        await self._session.close()

    @staticmethod
    async def _check_error(status_code: int, errors: dict):
        for error_code in errors.keys():
            if status_code == error_code:
                error = errors[error_code][0]
                error_text = errors[error_code][1]
                raise error(error_text)

    async def get_member_count(self, guild_id: int, days: int) -> dict:
        """Indicates the number of members on the guild on the respective day.

        Parameters
        ----------
        guild_id:
            The guild id from the guild.
        days:
            The number of days.
        """
        await self._check_session()
        async with self._session.get(
            BASE_URL + f"/members/{guild_id}?days={days}", headers=self._header
        ) as response:
            await self._close()
            await self._check_error(response.status, {401: (NotOwner, "The API key owner is not a member of the guild.")})
            data = await response.json()
            return data

    async def get_user_stats(self, user_id: int) -> UserStats:
        """Stats for a user.

        Parameters
        ----------
        user_id:
            The user's ID.
        """
        await self._check_session()
        async with self._session.get(
            BASE_URL + f"/stats/user/{user_id}", headers=self._header
        ) as response:
            await self._close()
            await self._check_error(response.status, {404: (UserNotFound, USER_NOT_FOUND_TEXT)})
            data = await response.json()
            user = UserStats(
                user_id,
                data.get("max_streak"),
                data.get("streak"),
                data.get("cookies"),
                data.get("career"),
                data.get("total_shifts"),
                data.get("job"),
            )
            return user

    async def get_member_activity(
        self, user_id: int, guild_id: int, days: int = 0
    ) -> MemberStats | MemberActivity:
        """If days is not provided or is 0, it will return the user's level stats.
        If days is provided, it will return the user's activity stats for the last x days.

        Parameters
        ----------
        user_id:
            The user id from the user.
        guild_id:
            The guild id from the guild.
        days:
            The number of days.
            Defaults to ``0``.
        """
        await self._check_session()
        async with self._session.get(
            BASE_URL + f"/stats/user/{user_id}/{guild_id}?days={days}", headers=self._header
        ) as response:
            await self._close()
            await self._check_error(
                response.status,
                {
                    404: (UserNotFound, USER_NOT_FOUND_TEXT),
                    401: (GuildNotFound, GUILD_NOT_FOUND_TEXT),
                })
            data = await response.json()
            if days == 0:
                user = MemberStats(
                    user_id,
                    guild_id,
                    data.get("lvl"),
                    data.get("xp"),
                    data.get("msg_count"),
                    data.get("voice_min"),
                    data.get("voice_xp"),
                    data.get("voice_lvl"),
                    data.get("current_lvl_progress"),
                    data.get("current_lvl_end"),
                    data.get("rank"),
                    data.get("member_count"),
                    data.get("voice_rank"),
                    data.get("voice_count"),
                )
            else:
                user = MemberActivity(
                    days,
                    user_id,
                    guild_id,
                    data.get("days_messages"),
                    data.get("days_voice_minutes"),
                    data.get("days_msg_rank"),
                    data.get("days_voice_rank"),
                    data.get("current_voice_min"),
                )
            return user

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
        await self._check_session()
        async with self._session.get(
            BASE_URL + f"/stats/guild/{guild_id}?days={days}", headers=self._header
        ) as response:
            await self._close()
            await self._check_error(
                response.status, {401: (GuildNotFound, GUILD_NOT_FOUND_TEXT)}
            )
            data = await response.json()
            guild = GuildActivity(
                days,
                data.get("messages"),
                data.get("total_messages"),
                data.get("total_voice_min"),
                data.get("top_channel"),
                data.get("top_channel_messages"),
                data.get("most_active_user_day"),
                data.get("most_active_user_hour"),
            )
            return guild
