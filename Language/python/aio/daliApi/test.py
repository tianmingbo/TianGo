# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: test.py
@time: 2024/1/21  20:30
@desc: 
"""
import asyncio

from dali.utils import aiofile


async def d():
    a = await aiofile.exists(
        '/Users/tianmingbo/PycharmProjects/GOOD-GOOD-STUDY/python/aio/daliApi/languages/zh-CN.json')
    print(a)


asyncio.run(d())
