import asyncio
import aiohttp


async def send_message(session, message):
    async with session.post('http://localhost:8080', data=message) as response:
        return await response.text()


async def main():
    messages = ['Hello' for _ in range(10)]

    async with aiohttp.ClientSession() as session:
        tasks = [send_message(session, message) for message in messages]
        results = await asyncio.gather(*tasks)

    # 处理结果
    for result in results:
        print(f"Received: {result}")


if __name__ == '__main__':
    asyncio.run(main())
