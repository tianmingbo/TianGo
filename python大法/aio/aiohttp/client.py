# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: client.py
@time: 2024/1/7  14:41
@desc: aiohttp client
"""
import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8080') as resp:
            print(resp.status)
            print(await resp.text())


if __name__ == '__main__':
    asyncio.run(main())
