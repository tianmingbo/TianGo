# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: __init__.py.py
@time: 2024/1/9  22:21
@desc: 
"""
from dali.handlers import dynamic_handler
from dali.handlers.error_pages import send_404_error
from dali.handlers.lifespan_handler import handle_lifespan
from dali.handlers.static_file_handler import handle_static_file_request
from dali.socketio import sio_asgi_app
from dali.utils.log import Log
from asgiref.wsgi import WsgiToAsgi


def wsgi(env, start_response):
    status = '200 OK'
    output = b'WSGI'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [output]


# 将wsgi包装为ASGI
wsgi_to_asgi_app = WsgiToAsgi(wsgi)


async def app(scope, receive, send):
    log = Log.get_instance()
    req_type = scope['type']
    if req_type == 'http':
        if scope['path'].startswith('/socket.io'):
            return await sio_asgi_app(scope, receive, send)
        if scope['path'].startswith('/wsgi'):
            return await wsgi_to_asgi_app(scope, receive, send)
        # data_sent = False
        data_sent = await dynamic_handler.handle_dynamic_request(scope, receive, send)
        if not data_sent:
            data_sent = await handle_static_file_request(scope, send)
        if not data_sent:
            await send_404_error(scope, receive, send)
    elif req_type == 'websocket':
        return await sio_asgi_app(scope, receive, send)
    elif req_type == 'lifespan':
        await handle_lifespan(scope, receive, send)
    else:
        log.warning('unknown request type: %s' % req_type)
