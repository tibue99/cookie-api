import io

import pytest
from PIL import Image

import cookie

# from cookie import api as cookie_api
# cookie_api.BASE_URL = "http://localhost:8000/v1/"


USER_ID = 203208036053942272
GUILD_ID = 1010915072694046794

INVALID_USER_ID = 12345
INVALID_GUILD_ID = 54321


def test_sync_api():
    api = cookie.CookieAPI()
    guild_stats = api.get_guild_stats(GUILD_ID)
    assert isinstance(guild_stats, cookie.GuildStats)

    user_stats = api.get_user_stats(USER_ID)
    assert isinstance(user_stats, cookie.UserStats)

    member_stats = api.get_member_stats(USER_ID, GUILD_ID)
    assert isinstance(member_stats, cookie.MemberStats)

    member_activity = api.get_member_activity(USER_ID, GUILD_ID)
    assert isinstance(member_activity, cookie.MemberActivity)

    guild_activity = api.get_guild_activity(GUILD_ID)
    assert isinstance(guild_activity, cookie.GuildActivity)

    guild_image = api.get_guild_image(GUILD_ID)
    img = Image.open(io.BytesIO(guild_image))
    assert isinstance(img, Image.Image)

    member_image = api.get_member_image(USER_ID, GUILD_ID)
    img = Image.open(io.BytesIO(member_image))
    assert isinstance(img, Image.Image)

    with pytest.raises(cookie.NotFound):
        api.get_user_stats(INVALID_USER_ID)


@pytest.mark.asyncio
async def test_async_api():
    async_api = cookie.AsyncCookieAPI()

    async with async_api as api:
        guild_stats = await api.get_guild_stats(GUILD_ID)
        assert isinstance(guild_stats, cookie.GuildStats)

        user_stats = await api.get_user_stats(USER_ID)
        assert isinstance(user_stats, cookie.UserStats)

        member_stats = await api.get_member_stats(USER_ID, GUILD_ID)
        assert isinstance(member_stats, cookie.MemberStats)

        member_activity = await api.get_member_activity(USER_ID, GUILD_ID)
        assert isinstance(member_activity, cookie.MemberActivity)

        guild_activity = await api.get_guild_activity(GUILD_ID)
        assert isinstance(guild_activity, cookie.GuildActivity)

        guild_image = await api.get_guild_image(GUILD_ID)
        img = Image.open(io.BytesIO(guild_image))
        assert isinstance(img, Image.Image)

        member_image = await api.get_member_image(USER_ID, GUILD_ID)
        img = Image.open(io.BytesIO(member_image))
        assert isinstance(img, Image.Image)

        with pytest.raises(cookie.NotFound):
            await api.get_user_stats(INVALID_USER_ID)


@pytest.mark.asyncio
async def test_invalid_keys():
    invalid_key = "invalid_key"

    with pytest.raises(cookie.InvalidAPIKey):
        api = cookie.CookieAPI(api_key=invalid_key)
        api.get_guild_stats(GUILD_ID)

    with pytest.raises(cookie.InvalidAPIKey):
        async_api = cookie.AsyncCookieAPI(api_key=invalid_key)
        async with async_api as api:
            await api.get_guild_stats(GUILD_ID)
