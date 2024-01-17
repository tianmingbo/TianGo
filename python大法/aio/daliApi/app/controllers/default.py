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
    print(req.get_var_as_str(b'name'))
    print(req.get_var_as_str(b'pwd'))
    await res.end(b'default page')


class Hello:
    # 接受调用
    @cache()
    async def __call__(self, req: Request, res: Response):
        await res.end(b'default page')


async def get_args(req: Request, res: Response):
    await res.write(b'Args is ')
    await res.end(','.join(req.args).encode('utf-8'))
