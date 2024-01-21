# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: reponse.py
@time: 2024/1/14  21:22
@desc: Response
"""
import config
from dali.http.request import Request


class Response:
    def __init__(self, request: Request, send):
        self._send = send
        self._content_type = b'text/html'  # 用来记录返回的content_type类型
        self._request: Request = request
        self._header_sent = False  # 指示头部是否已发送
        self._body_sent = False  # 指示body是否已发送
        self._body = b''
        self._headers_map = {b'server': config.SERVER_NAME}  # 返回的header
        self.set_cookie(config.SESSION_ID_KEY, self._request.session_id_str)

    @property
    def header_sent(self):
        return self._header_sent

    @property
    def body_sent(self):
        return self._body_sent

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value: bytes):
        self._content_type = value
        self._headers_map[b'content-type'] = [value]

    @property
    def body(self):
        return self._body

    def _get_headers(self):
        res = []
        for key in self._headers_map:
            for v in self._headers_map[key]:
                res.append([key, v])
        return res

    async def send_header(self, status_code=200):
        await self._send({
            'type': 'http.response.start',
            'status': status_code,
            'headers': self._get_headers()
        })
        self._header_sent = True

    async def write(self, data: bytes):
        if not self._header_sent:
            await self.send_header()
        await self._send({
            'type': 'http.response.body',
            'body': data,
            # 为True，表示还有后续内容发送
            'more_body': True
        })

    async def end(self, data: bytes):
        if self._body_sent:
            return
        if not self._header_sent:
            await self.send_header()
        await self._send({
            'type': 'http.response.body',
            'body': data,
            'more_body': False
        })
        self._body = data
        self._body_sent = True

    def add_header(self, key: bytes, value: bytes):
        if key not in self._headers_map:
            self._headers_map[key] = []
        self._headers_map[key].append(value)

    def set_cookie(self, name: str, value: str, max_age: int = 604800, path: bytes = b'/'):
        """
        设置cookie
        :param name:
        :param value:
        :param max_age:
        :param path:
        :return:
        """
        self.add_header(
            b'set-cookie',
            '{name}={value}; Max-Age={max_age}; Path={path}'.format(
                name=name,
                value=value,
                max_age=max_age,
                path=path
            ).encode(config.GLOBAL_CHARSET)
        )
