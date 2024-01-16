# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: request.py
@time: 2024/1/14  21:24
@desc:  Request
"""
import re

import config


class Request:
    def __init__(self, scope, receive):
        self._scope = scope
        self._receive = receive
        self._args = None
        self._protocol = scope['scheme']  # http or https
        self._method = scope['method']  # 请求方法
        self._path = scope['path']  # 请求路径
        self._query_string = scope['query_string']  # 请求路径中？后面的参数
        self._raw_headers = scope['headers'] if 'headers' in scope else []
        self._headers = {}
        self._parse_header()
        self._raw_accept_languages = self.get_header(b'accept-language')
        self._accept_languages = re.compile(b"[a-z]{2}-[A-Z]{2}").findall(
            self._raw_accept_languages
        ) if self._raw_accept_languages else []
        lang = config.LANGUAGE or (
            self._accept_languages[0] if self._accept_languages else b'zh-CN')
        self._language = lang.decode('utf-8')

        self._content_type = None
        self._uri = None  # 请求的uri
        self._host = self.get_header(b'host')
        self._client = self._scope['client']
        self._client_ip = self._client[0]
        self._client_port = self._client[1]
        self._controller = None  # 记录请求的控制器名
        self._action = None  # 记录请求的函数名

    @property
    def headers(self):
        return self._headers

    @property
    def args(self):
        """所有的路径参数"""
        return self._args

    def arg(self, index):
        """
        返回指定位置的参数
        :param index:
        :return:
        """
        return self._args[index] if self.args and len(self.args) > index else None

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    @property
    def host(self):
        return self._host

    @property
    def client_ip(self):
        return self._client_ip

    @property
    def protocol(self):
        return self._protocol

    @property
    def path(self):
        return self._path

    @property
    def query_string(self):
        return self._query_string

    @property
    def accept_languages(self):
        return self._accept_languages

    @property
    def language(self):
        return self._language

    @property
    def content_type(self):
        if not self._content_type:
            self._content_type = self.get_header(b'content-type')
        return self._content_type

    @property
    def method(self):
        return self._method

    @property
    def uri(self):
        if not self._uri:
            self._uri = self.path
            if self.query_string:
                self._uri += "?"
                self._uri += self.query_string.decode(config.GLOBAL_CHARSET)
        return self._uri

    def _parse_header(self):
        for header in self._raw_headers:
            if len(header) == 2:
                key = header[0]
                if key not in self._headers:
                    self._headers[key] = []
                self._headers[key].append(header[1])

    @staticmethod
    def _get_first_value_of_array(data, key):
        values = data[key] if (data and key in data) else None
        value = None
        if values:
            value = values[0]
        return value

    def get_header(self, key: bytes, default=None) -> bytes:
        return self._get_first_value_of_array(self.headers, key) or default

    def get_headers(self, key: bytes):
        return self.headers[key] if key in self.headers else None

    def is_mobile(self):
        user_agent = self.get_header(b'user-agent')
        if user_agent:
            return user_agent.find(b'iPhone') != -1 or \
                user_agent.find(b'Android') != -1 or \
                user_agent.find(b'iPod') != -1
        return False
