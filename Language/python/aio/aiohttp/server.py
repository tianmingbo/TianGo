# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: server.py
@time: 2024/1/7  14:22
@desc: 使用aiohttp实现异步web服务器
"""
import base64

from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

routers = web.RouteTableDef()


async def hello(request: web.Request):
    session = await get_session(request)
    session['count'] = session.get('count', 0) + 1
    return web.Response(text=f"Count is {session['count']}")


@routers.get("/{name}")
async def user(request: web.Request):
    name = request.match_info.get('name', "Anonymous")
    return web.Response(text=f"Hello, {name}")


app = web.Application()
app.router.add_get("/", hello)
app.add_routes(routers)
# 使用session
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))
web.run_app(app)
