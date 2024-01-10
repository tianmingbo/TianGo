# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: error_pages.py
@time: 2024/1/10  22:27
@desc: 
"""


async def send_404_error(scope, receive, send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [
                [b"content-type", b"text/html"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"<h1>404 Not Found</h1>",
            "more_body": False,
        }
    )
