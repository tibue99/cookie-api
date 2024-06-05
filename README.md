# CookieBot API
### Official API wrapper for the CookieBot API
Python 3.9 or higher is required
```
pip install cookiebot
```
## Example Usage
````python
import asyncio
from cookiebot import CookieAPI

api = CookieAPI(api_key="[YOUR_API_KEY]")

async def start():
    user = await api.get_user_stats(123456789)
    print(user) # UserStats(user_id=123456789, max_streak=334, streak=334, cookies=18539, career='Cookie Producer', total_shifts=487, job='Cookie Head Chef')

    await api.close()

asyncio.run(main())
````


### Activity for a time period
````python
member_activity = await api.get_member_activity(887307645529231431, 1010915072694046794, days=14)
````

### Member count history
````python
activity = await api.get_member_count(1010915072694046794, days=3)
print(activity)  # {'2024-06-01': 1310, '2024-06-02': 1311, '2024-06-03': 1311}
````
