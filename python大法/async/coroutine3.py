import asyncio
import requests


async def request():
    res = requests.get('https://www.baidu.com')
    return res.status_code


def callback(task):
    print('status_code', task.result())


coroutine = request()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)  # 添加回调函数
print('task', task)

loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('task end', task)
# print(task.result())  # 也可以直接获得结果，不使用回调函数
