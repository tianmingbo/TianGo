# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: default.py
@time: 2024/1/15  20:40
@desc: 
"""
from dali.cache import cache
from dali.http import Response, Request


@cache(expire=5)
async def index(req: Request, res: Response):
    await res.end(b'default page')


async def login(req: Request, res: Response):
    words = await res.translate("Home")
    await res.end("你好".encode('gbk'))


async def counter(req: Request, res: Response):
    count = int(await req.get_session('count') or '0')
    count += 1
    await req.set_session('count', count)
    await res.end(b'count is %s' % str(count).encode('utf-8'))


class Hello:
    # 接受调用
    @cache()
    async def __call__(self, req: Request, res: Response):
        await res.end(b'default page')


async def get_args(req: Request, res: Response):
    await res.write(b'Args is ')
    await res.end(','.join(req.args).encode('utf-8'))
