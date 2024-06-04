# CookieBot API
### Official API wrapper for the CookieBot API
```
pip install cookiebot
```
## Examples
### Define API
````python
from cookiebot import CookieAPI

api = CookieAPI(api_key="[YOUR_API_KEY]")
````
### User Stats
````python
import asyncio

async def start():
    response = await api.get_user_stats(887307645529231431)
    print(response) # UserStats(user_id=887307645529231431, max_streak=334, streak=334, cookies=18539, career='Cookie Producer', total_shifts=487, job='Cookie Head Chef')

asyncio.run(start())
````
### Member Stats
````python
import asyncio

async def start():
    response = await api.get_member_stats(887307645529231431, 1010915072694046794)
    print(response) # MemberStats(user_id=887307645529231431, guild_id=1010915072694046794, level=38, xp=71028, msg_count=7741, voice_min=96761, voice_xp=290283, voice_level=76, current_level_progress=728, current_level_end=3800, msg_rank=9, msg_total_members=1835, voice_rank=2, voice_total_members=674)

asyncio.run(start())
````
### Memeber Activity
````python
import asyncio

async def start():
    response = await api.get_member_activity(887307645529231431, 1010915072694046794, days=14)

    print(response) # MemberActivity(days=14, user_id=887307645529231431, guild_id=1010915072694046794, msg_count=352, voice_min=5836, msg_rank=4, voice_rank=1, current_voice_minutes=12)

asyncio.run(start())
````

### Guild Members
````python
import asyncio

async def start():
    response = await api.get_member_count(1010915072694046794, days=3)
    print(response)  # {'2024-06-01': 1310, '2024-06-02': 1311, '2024-06-03': 1311}

asyncio.run(start())
````
