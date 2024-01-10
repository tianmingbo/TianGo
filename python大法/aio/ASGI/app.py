# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: app.py
@time: 2024/1/7  14:57
@desc: 基于ASGI的demo
"""
import uvicorn


async def app(scope, receive, send):
    request_type = scope['type']
    if request_type == 'http':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']]
        })
        await send({
            'type': 'http.response.body',
            'body': b'Hello, world!',
            'more_body': False
        })
    elif request_type == 'websocket':
        await send({
            'type': 'websocket.accept'
        })
    elif request_type == 'lifespan':
        # 生命周期管理接口，侦听服务器的启动与关闭
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                print('server start!')
                await send({
                    'type': 'lifespan.startup.complete'
                })
            elif message['type'] == 'lifespan.shutdown':
                print('server shutdown!')
                await send({
                    'type': 'lifespan.shutdown.complete'
                })
                break
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
