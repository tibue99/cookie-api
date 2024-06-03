# CookieBot API
### Official API wrapper for the Cookie Bot API
```
pip install cookiebot
```
## Examples
### User Stats
````python
from cookiebot import CookieAPI
import asyncio

api = CookieAPI(api_key="[YOUR_API_KEY]", raise_error=True)

async def start():
    response = await api.get_user_stats(887307645529231431)
    print(response)

asyncio.run(start())
````
This prints:
````python
User(user_id=887307645529231431, max_streak=334, streak=334, cookies=18539, career='Cookie Producer', total_shifts=487, job='Cookie Head Chef')
````
### Guild Stats
````python
from cookiebot import CookieAPI
import asyncio

api = CookieAPI(api_key="[YOUR_API_KEY]", raise_error=True)

async def start():
    response = await api.get_guild_stats(1010915072694046794, days=2)
    print(response)

asyncio.run(start())
````
This prints:
````python
Guild(messages={'2024-06-02': 386, '2024-06-03': 40}, total_messages=426, total_voice_minutes=2495, top_channel=1019643517573799936, top_channel_messages=40, most_active_user_day=887307645529231431, most_active_user_hour=None)
````
### 
````python
from cookiebot import CookieAPI
import asyncio

api = CookieAPI(api_key="[YOUR_API_KEY]", raise_error=True)

async def start():
    response = await api.get_user_guild_stats(887307645529231431, 1010915072694046794)
    with_days = await api.get_user_guild_stats(887307645529231431, 1010915072694046794, days=14)
    print(response)
    print(with_days)

asyncio.run(start())
````
This prints:
````python
UserGuild(user_id=887307645529231431, guild_id=1010915072694046794, level=38, xp=70623, msg_count=7707, voice_min=96297, voice_xp=288891, voice_level=76, current_level_progress=323, current_level_end=3800, rank=9, rank_total=1829, voice_rank=2, voice_rank_total=672)
UserStat(user_id=887307645529231431, guild_id=1010915072694046794, messages=334, voice_minutes=5799, message_rank=5, voice_rank=1, current_voice_minutes=0)
````
### Guild Members
````python
from cookiebot import CookieAPI
import asyncio

api = CookieAPI(api_key="[YOUR_API_KEY]", raise_error=True)

async def start():
    response = await api.get_guild_members(1010915072694046794, days=3)
    print(response)

asyncio.run(start())
````
This prints:
````python
{'2024-06-01': 1310, '2024-06-02': 1311, '2024-06-03': 1311}
````