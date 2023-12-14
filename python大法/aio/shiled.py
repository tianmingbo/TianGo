import asyncio

from util.py.async_timed import async_timed


@async_timed
async def delay(seconds):
    print(f"开始休眠 {seconds} 秒")
    await asyncio.sleep(seconds)
    print(f"休眠完成")
    return seconds


@async_timed
async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        # 通过 asyncio.shield 将 delay_task 保护起来
        result = await asyncio.wait_for(asyncio.shield(delay_task), 1)
        print("返回值:", result)
    except asyncio.TimeoutError:
        print("超时啦")
        # 如果超时依旧会引发 TimeoutError，但和之前不同的是
        # 此时任务不会被取消了，因为 asyncio.shield 会将取消请求忽略掉
        print("任务是否被取消:", delay_task.cancelled())
        # 从出现超时的地方，继续执行，并等待它完成
        result = await delay_task
        print("返回值:", result)


asyncio.run(main())
"""
开始休眠 2 秒
超时啦
任务是否被取消: False
休眠完成
返回值: 2
"""
