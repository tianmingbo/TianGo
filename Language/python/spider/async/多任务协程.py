import asyncio
import random
import time
import requests


async def request():
    res = requests.get('https://www.baidu.com')
    time.sleep(random.randint(1, 3))
    return res.status_code


tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
for task in tasks:
    print(task.result())
