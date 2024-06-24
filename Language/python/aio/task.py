import asyncio


async def delay(seconds):
    print(f"开始休眠 {seconds} 秒")
    await asyncio.sleep(seconds)
    print(f"休眠完成")
    return seconds


async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, 1)
        print("返回值:", result)
    except asyncio.TimeoutError:
        print("超时啦")
        # delay_task.cancelled() 用于判断任务是否被取消
        # 任务被取消：返回 True，没有被取消：返回 False
        print("任务是否被取消:", delay_task.cancelled())


asyncio.run(main())
"""
开始休眠 2 秒
超时啦
任务是否被取消: True
"""
