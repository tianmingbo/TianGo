# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: sio_events.py
@time: 2024/1/22  21:51
@desc: socket.io
"""
import asyncio

from dali.socketio import sio


async def echo_task(sid):
    for i in range(6):
        await sio.emit('counter', i, sid)
        await asyncio.sleep(1)


@sio.event
async def connect(sid, environ):
    asyncio.create_task(echo_task(sid))
