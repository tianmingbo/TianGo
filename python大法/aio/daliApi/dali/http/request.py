# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: request.py
@time: 2024/1/14  21:24
@desc:  Request
"""
import json
import re

import config
from dali.utils.log import Log
from dali.utils.url_helper import parse_url_pairs


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
        self._body = b''
        self._uri = None  # 请求的uri
        self._host = self.get_header(b'host')
        self._client = self._scope['client']
        self._client_ip = self._client[0]
        self._client_port = self._client[1]
        self._controller = None  # 记录请求的控制器名
        self._action = None  # 记录请求的函数名
        self._query_vars = {}  # 路径中的参数
        self._body_vars = {}  # 协议内容中的参数

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
    def query_vars(self):
        return self._query_vars

    @property
    def body_vars(self):
        return self._body_vars

    @property
    def uri(self):
        if not self._uri:
            self._uri = self.path
            if self.query_string:
                self._uri += "?"
                self._uri += self.query_string.decode(config.GLOBAL_CHARSET)
        return self._uri

    def get_query_vars(self, key: bytes) -> list:
        """
        根据键名获取所有的值
        :param key:
        :return:
        """
        return self.query_vars[key] if key in self.query_vars else None

    def get_query_var(self, key: bytes, default=b'') -> bytes:
        """
        根据键名获取匹配的第一个值
        :param key:
        :param default:
        :return:
        """
        return self._get_first_value_of_array(self.query_vars, key) or default

    def get_body_vars(self, key: bytes) -> list:
        """
        根据键名获取所有消息体参数
        :param key:
        :return:
        """
        return self.body_vars[key] if key in self.body_vars else None

    def get_body_var(self, key: bytes, default=b'') -> bytes:
        """
        根据键名获取匹配的第一个消息体参数
        :param key:
        :param default:
        :return:
        """
        return self._get_first_value_of_array(self.body_vars, key) or default

    def get_var(self, key: bytes, default=b'') -> bytes:
        """
        从消息体活URL中获取参数
        :param key:
        :param default:
        :return:
        """
        if self.method == 'GET':
            return self.get_query_var(key, default)
        elif self.method == 'POST':
            return self.get_body_var(key, default) or self.get_query_var(key, default)
        return default

    def get_var_as_str(self, key: bytes, default='', charset=config.GLOBAL_CHARSET) -> str:
        var = self.get_var(key)
        if var:
            return var.decode(charset)
        return default

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

    async def parse_form(self):
        """
        表单解析
        application/x-www-form-urlencoded
        multipart/form-data
        text/plain
        :return:
        """
        if self._query_string:
            self._query_vars = parse_url_pairs(self._query_string)
        if self.method == 'POST':
            while True:
                message = await self._receive()
                self._body += message['body'] if 'body' in message else b''
                if 'more_body' not in message or not message['more_body']:
                    break
            if self.content_type:
                # application/x-www-form-urlencoded类型以参数对得方式解析
                if self.content_type.startswith(b'application/x-www-form-urlencoded'):
                    self._body_vars = parse_url_pairs(self._body)
                elif self.content_type.startswith(b'multipart/form-data'):
                    boundary = re.search(b'multipart/form-data; boundary=(.*)', self.content_type)
                    if boundary:
                        boundary = boundary.group(1)
                        if self._body:
                            body_results = self._body.split(b'\r\n--' + boundary)
                            if body_results:
                                for body_res in body_results:
                                    split_index = body_res.find(b'\r\n\r\n')
                                    if split_index != -1:
                                        # 获取头部信息字符串
                                        head = body_res[:split_index]
                                        # 获取内容
                                        content = body_res[split_index + 4:]
                                        # 取出该字段的key
                                        key = re.search(b'Content-Disposition: form-data; name="(.*?)"', head)
                                        if key:
                                            key = key.group(1)
                                            if key not in self._body_vars:
                                                self._body_vars[key] = []
                                            # 如果是文件，获取文件名
                                            filename = re.search(b'filename="(.*)"', head)
                                            file_name = filename.group(1) if filename else None
                                            if not file_name:
                                                # 如果不是文件，则值为普通字符串
                                                self._body_vars[key].append(content)
                                            else:
                                                file_obj = {
                                                    'filename': file_name,
                                                    'content': content,
                                                    'name': key
                                                }
                                                # 获取文件类型
                                                content_type = re.search(b'Content-Type: (.*)', head)
                                                if content_type:
                                                    file_obj['content'] = content_type.group(1)
                                                self._body_vars[key].append(file_obj)
                                    else:
                                        break
                elif self.content_type.startswith(b'application/json'):
                    Log.get_instance().info(json.loads(self._body))
                else:
                    Log.get_instance().info(f'{self.content_type} we can not parse')
            else:
                Log.get_instance().warning('content-type is None')
