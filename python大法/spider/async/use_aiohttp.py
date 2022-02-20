# import asyncio
# import aiohttp
# from aiohttp import TCPConnector
# import time
#
# start = time.time()
#
#
# async def get(url):
#     session = aiohttp.ClientSession(connector=TCPConnector(ssl=False))  # 取消ssl验证
#     res = await session.get(url)
#     await res.text()
#     await session.close()
#     return res.status
#
#
# async def request():
#     url = 'https://www.baidu.com'
#     print('waiting for ', url)
#     res = await get(url)
#     print(res)
#
#
# tasks = [asyncio.ensure_future(request()) for _ in range(1000)]  # 启动1000个协程
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
# end = time.time() - start
# print(end)


##################################华丽的分界线########################################
# import asyncio
# import aiohttp
# from aiohttp import TCPConnector
#
#
# async def fetch(session, url):
#     data = {'1': 1}
#     async with session.post(url, data=data) as res:  # 携带参数
#         print(await res.text(), await res.read(), await res.json())
#         return await res.text(), res.status  # res.text()是协程对象，所以需要await
#
#
# async def main():
#     timeout = aiohttp.ClientTimeout(total=10)  # 设置超时时间
#     async with aiohttp.ClientSession(timeout=timeout, connector=TCPConnector(ssl=False)) as session:
#         text, status = await fetch(session, 'https://www.httpbin.org/post')
#         print(text)
#         print(status)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
##################################华丽的分界线########################################


import asyncio
import aiohttp
from aiohttp import TCPConnector

CONCURRENCY = 5
url = 'https://www.baidu.com'

semaphore = asyncio.Semaphore(CONCURRENCY)  # 创建一个信号量，控制最大并发个数
session = None


async def scrape_api():
    async with semaphore:
        print('scraping', url)
        async with session.get(url) as res:
            await asyncio.sleep(1)
            print(res.status)
            return await res.text()


async def main():
    global session
    session = aiohttp.ClientSession(connector=TCPConnector(ssl=False))
    scrape_index_tasks = [asyncio.ensure_future(scrape_api()) for _ in range(10000)]
    await asyncio.gather(*scrape_index_tasks)  # 启动协程


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
