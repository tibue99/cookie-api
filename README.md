# CookieBot API
Official wrapper for the [CookieBot](https://cookie-bot.xyz) API.

## ⚙️ Installation
Python 3.9 or higher is required
```
pip install cookiebot
```

## 🔑 How to get an API key?
1. Invite [CookieBot](https://cookie-bot.xyz) to your Discord server
2. Run `/premium api`

## 🚀 Example Usage
```python
import asyncio
from cookiebot import CookieAPI

api = CookieAPI(api_key="[YOUR_API_KEY]")

async def main():
    user_stats = await api.get_user_stats(123456789)  # Replace with user ID
    await api.close()

asyncio.run(main())
```
You can also use an asynchronous context manager (recommended)
```python
async def main():
    async with api as con:
        user_stats = await con.get_user_stats(123456789)  # Replace with user ID
```
