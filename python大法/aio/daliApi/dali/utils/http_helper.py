# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: http_helper.py
@time: 2024/1/14  20:45
@desc: http协议字符串处理
"""
import time
from datetime import datetime

import config


def timestamp_to_http_time(timestamp) -> bytes:
    # 将时间戳转换为 datetime 对象
    dt = datetime.utcfromtimestamp(timestamp).replace()

    # 格式化为 HTTP 标准协议时间字符串
    http_time = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return http_time.encode(config.GLOBAL_CHARSET)
