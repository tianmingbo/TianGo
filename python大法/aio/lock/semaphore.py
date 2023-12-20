"""
信号量是一种可在这些情况下帮助我们完成任务的结构，它的作用很像锁，但可以被多次获取。
信号量内部有一个可以设定的初始值，每次获取（acquire）时，内部的值会减 1，释放（release）时则加 1。如果这个值为 0，
那么再次获取信号量时会发生阻塞。所以如果和Lock做对比的话，可以把锁看作是内部初始值为 1 的信号量。
"""

import asyncio
from asyncio import Semaphore
from aiohttp import ClientSession


async def get_status(url: str,
                     session: ClientSession,
                     sem: Semaphore):
    print(f"等待获取信号量")
    async with sem:
        print("信号量已获取, 正在发送请求")
        response = await session.get(url)
        print("请求已完成")
        return response.status


async def main():
    sem = Semaphore(10)  # 并发为10
    async with ClientSession() as session:
        tasks = [get_status("http://www.baidu.com", session, sem) for _ in range(1000)]
        await asyncio.gather(*tasks)


asyncio.run(main())
