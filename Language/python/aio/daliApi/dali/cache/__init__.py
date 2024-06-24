# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: __init__.py.py
@time: 2024/1/15  21:13
@desc: 
"""
from datetime import datetime

from dali.utils.log import Log
from dali.cache.base_cache_manager import CacheDataWrapper, BaseCacheManager
from dali.cache.modules_cache_manager import ModulesCacheManager
from dali.cache.page_cache_manager import PageCacheManager
from dali.cache.session_cache_manager import SessionCacheManager


def cache(expire=3600, key=None):
    """
    为想要添加缓存的页面添加该装饰器
    :param expire:  过期时间 s
    :param key: 缓存键
    :return:
    """

    def wrapper(target):
        async def inner(*args):
            argc = len(args)
            if argc == 2:
                # 参数个数为2，装饰的是函数
                req = args[0]
                res = args[1]
            elif args == 3:
                # 参数个数为3，装饰的是方法
                req = args[1]
                res = args[2]
            else:
                raise TypeError('require 2 or 3 arguments')
            _key = key
            if not _key:
                # 如果没有指定键，使用uri作为缓存
                _key = req.uri
                # 移动端单独缓存
                if req.is_mobile():
                    _key += ',mobile'

            async def wrap_data_callback(cache_key) -> CacheDataWrapper:
                await target(*args)
                Log.get_instance().warning('cache key: %s' % _key)
                # 获取缓存数据
                return CacheDataWrapper(res.body, datetime.now().timestamp() + expire)

            cache_data = await PageCacheManager.get_instance().get_data(_key, wrap_data_callback)
            if not res.body_sent:
                await res.end(cache_data)

        return inner

    return wrapper
