# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: __init__.py.py
@time: 2024/1/22  21:53
@desc: 
"""
import socketio
import os
import config
import importlib

sio = socketio.AsyncServer(async_mode='asgi')
sio_asgi_app = socketio.ASGIApp(sio)


async def load_sio_files():
    """
    加载sio文件
    :return:
    """
    sio_root = os.path.join(config.APP_DIR_NAME, config.SOCKET_IO_DIR_NAME)
    sio_files = os.listdir(sio_root)
    for sio_file in sio_files:
        if sio_file.endswith('.py'):
            sio_file = sio_file.replace('.py', '')
            # 导入模块
            importlib.import_module(f'{config.APP_DIR_NAME}.{config.SOCKET_IO_DIR_NAME}.{sio_file}')
