import aiohttp
import asyncio
import logging
import json
from aiohttp import TCPConnector
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')
index_utl = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
detail_utl = 'https://spa5.scrape.center/api/book/{id}'
PAGE_SIZE = 18
PAGE_NUMBER = 100
CONCURRENCY = 5
MONGO_CONNECTION_STRING = 'mongodb://admin:123456@******:27017'
MONGODB_NAME = 'book'
MONGODB_COLLECTION_NAME = 'books'
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGODB_NAME]
collection = db[MONGODB_COLLECTION_NAME]

semaphore = asyncio.Semaphore(CONCURRENCY)  # 信号量
session = None


async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url) as res:
                return await res.json()
        except aiohttp.ClientError:  # 捕获异常
            logging.error('error occured while scraping %s', url, exc_info=True)


async def scrape_index(page):
    # 获取列表页
    url = index_utl.format(offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url)


async def save_data(data):
    # 异步保存数据
    logging.info(f'save data:{data}')
    if data:
        return await collection.update_one({
            'id': data.get('id')
        }, {'$set': data}, upsert=True)


async def get_detail(id):
    # 获取详情页
    url = detail_utl.format(id=id)
    data = await scrape_api(url)
    await save_data(data)


async def main():
    global session
    session = aiohttp.ClientSession(connector=TCPConnector(ssl=False))
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
    results = await asyncio.gather(*scrape_index_tasks)
    # logging.info('results:%s', json.dumps(results, ensure_ascii=False, indent=2))
    ids = []
    # 获取id列表
    for index_data in results:
        if not index_data:
            continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_detail_tasks = [asyncio.ensure_future(get_detail(id)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)
    await session.close()  # 关闭session


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
