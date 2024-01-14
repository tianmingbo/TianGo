# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: __init__.py.py
@time: 2024/1/9  22:21
@desc: 
"""
import uvicorn

from dali.handlers.error_pages import send_404_error
from dali.handlers.lifespan_handler import handle_lifespan
from dali.handlers.static_file_handler import handle_static_file_request
from dali.utils.log import Log


async def app(scope, receive, send):
    log = Log.get_instance()
    req_type = scope['type']
    if req_type == 'http':
        data_sent = await handle_static_file_request(scope, send)
        if not data_sent:
            await send_404_error(scope, receive, send)
    elif req_type == 'lifespan':
        await handle_lifespan(scope, receive, send)
    else:
        log.warning('unknown request type: %s' % req_type)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
