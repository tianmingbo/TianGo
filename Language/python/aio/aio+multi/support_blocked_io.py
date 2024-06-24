"""
支持阻塞任务并发
"""
import asyncio
from concurrent import futures
import time


# 阻塞型任务
def block_task():
    for i in range(10):
        time.sleep(1)
        print(f'blocked and cur time is {time.time()}')


async def async_task():
    for i in range(2):
        await asyncio.sleep(5)
        print(f'async task and cur time is{time.time()}')


async def main():
    loop = asyncio.get_running_loop()
    # 创建一个线程池执行器，也可以不创建，run_in_executor来创建。
    # CPU密集型使用进程池执行器
    executor = futures.ThreadPoolExecutor(thread_name_prefix='test', max_workers=5)
    await asyncio.gather(
        loop.run_in_executor(executor, block_task),
        async_task()
    )


if __name__ == '__main__':
    asyncio.run(main())
