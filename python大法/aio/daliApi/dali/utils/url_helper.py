# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: url_helper.py
@time: 2024/1/16  22:32
@desc: get请求参数解析
"""


def parse_url_pairs(query_string: bytes):
    """
    b'name=tian&age=18'
    解码为字典
    :param query_string:
    :return:
    """
    params = {}
    tokens = query_string.split(b'&')
    for token in tokens:
        kv = token.split(b'=')
        if len(kv) == 2:
            k = kv[0]
            v = kv[1]
            if k not in params:
                params[k] = []
            params[k].append(v)
    return params
