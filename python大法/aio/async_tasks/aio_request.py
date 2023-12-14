import asyncio
import aiohttp

from util.py.aio_request import fetch_status
from util.py.async_timed import async_timed


@async_timed
async def main():
    async with aiohttp.ClientSession() as session:
        task1 = [fetch_status(session, "http://www.baidu.com") for _ in range(1000)]
        task2 = [fetch_status(session, "https://blog.csdn.net/T_I_A_N_/article/details/129082706") for _ in
                 range(50)]
        # return_exceptions 参数，默认为 False，当任务出现异常时，会抛给 await 所在的位置。
        # 如果该参数设置为 True，那么出现异常时，会直接把异常本身返回（此时任务也算是结束了）
        gather1 = asyncio.gather(*task1, return_exceptions=True)
        gather2 = asyncio.gather(*task2)
        # 可以继续接收 asyncio.gather 返回的对象，从而实现分组功能
        status_codes = await asyncio.gather(gather1, gather2)
        print(len(status_codes))
        print(status_codes)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""
协程 main 开始执行
100
协程 main 用 0.4120007 秒执行完毕
"""
