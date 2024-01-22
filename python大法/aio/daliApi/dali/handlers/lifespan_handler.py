# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: lifespan_handler.py
@time: 2024/1/10  22:28
@desc: 生命周期管理
"""
from dali.socketio import load_sio_files
from dali.utils.log import Log


async def handle_lifespan(scope, receive, send):
    log = Log.get_instance()
    while True:
        # 不断读取数据
        message = await receive()
        if message['type'] == 'lifespan.startup':
            log.info('lifespan.startup')
            await load_sio_files()
            await send({'type': 'lifespan.startup.complete'})
        elif message['type'] == 'lifespan.shutdown':
            log.info('lifespan.shutdown')
            await send({'type': 'lifespan.shutdown.complete'})
            break
