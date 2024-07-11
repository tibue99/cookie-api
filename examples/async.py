import asyncio

from cookiebot import AsyncCookieAPI

api = AsyncCookieAPI()  # API key is set in .env


async def main():
    async with api as con:
        user_stats = await con.get_user_stats(123456789)  # Replace with user ID
        print(user_stats)


asyncio.run(main())
