# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: default.py
@time: 2024/1/15  20:40
@desc: 
"""
from dali.http import Response, Request


async def index(req: Request, res: Response):
    await res.end(b'default page')


class Hello:
    # 接受调用
    async def __call__(self, req: Request, res: Response):
        await res.end(b'default page')
