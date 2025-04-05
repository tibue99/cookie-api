# Cookie API
[![](https://img.shields.io/pypi/v/cookie-api.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/cookie-api/)
[![](https://img.shields.io/pypi/l/cookie-api?style=for-the-badge&color=5865F2)](https://github.com/tibue99/cookie-api/blob/main/LICENSE)
[![](https://img.shields.io/readthedocs/cookie-api?style=for-the-badge)](https://cookie-api.readthedocs.io/)
[![](https://img.shields.io/badge/Cookie-Website-orange?style=for-the-badge)](https://cookieapp.me/)

Official wrapper for the [Cookie](https://cookieapp.me) API.

## ⚙️ Installation
Python 3.9 or higher is required
```
pip install cookie-api
```

## 🔑 How to get an API key?
1. Invite [Cookie](https://cookieapp.me) to your Discord server or to your Discord account
2. Run `/premium api`

## 🚀 Example Usage
The API key can be passed as a parameter or set as the environment variable `COOKIE_KEY`.
For more information, see to our [documentation](https://cookie-api.readthedocs.io/).

### Sync Example
```python
from cookie import CookieAPI

api = CookieAPI(api_key="[YOUR_API_KEY]")

user_stats = api.get_user_stats(123456789)  # Replace with user ID
```
### Async Example
```python
import asyncio
from cookie import AsyncCookieAPI

api = AsyncCookieAPI(api_key="[YOUR_API_KEY]")

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

## ⚡ OpenAPI Docs
If you want to use the API without this wrapper, you can find the OpenAPI docs [here](https://api.cookieapp.me/docs).

The models in this package are automatically generated using the OpenAPI spec:
```
python cookie/_internal/model_generator.py
```
