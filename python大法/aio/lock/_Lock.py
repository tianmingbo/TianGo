import asyncio
from asyncio import Lock


async def a(lock: Lock):
    print("协程 a 等待获取锁")
    async with lock:
        print("协程 a 成功获取了锁, 并进入临界区执行操作")
        await asyncio.sleep(2)
    print("协程 a 释放了锁")


async def b(lock: Lock):
    print("协程 b 等待获取锁")
    async with lock:
        print("协程 b 成功获取了锁, 并进入临界区执行操作")
        await asyncio.sleep(2)
    print("协程 b 释放了锁")


async def main():
    lock = Lock()
    await asyncio.gather(a(lock), b(lock))


asyncio.run(main())
"""
协程 a 等待获取锁
协程 a 成功获取了锁, 并进入临界区执行操作
协程 b 等待获取锁
协程 a 释放了锁
协程 b 成功获取了锁, 并进入临界区执行操作
协程 b 释放了锁
"""
