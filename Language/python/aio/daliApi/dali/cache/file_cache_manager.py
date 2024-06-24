# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: page_cache_manager.py
@time: 2024/1/21  18:46
@desc:  文件缓存
"""

from dali.cache import BaseCacheManager, CacheDataWrapper
from dali.utils import aiofile


class FileCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "FileCacheManager":
        if FileCacheManager.__instance is None:
            FileCacheManager.__instance = FileCacheManager()
        return FileCacheManager.__instance

    async def wrap_data(self, key) -> CacheDataWrapper:
        wrapper = None
        if await aiofile.exists(key) and await aiofile.is_file(key):
            content = await aiofile.read_file(key)
            # 将文件与对应的修改时间包装成缓存数据包装器
            wrapper = CacheDataWrapper(content, await aiofile.get_mtime(key))
        return wrapper

    async def will_reload(self, wrapper: CacheDataWrapper, key: str) -> bool:
        return await aiofile.exists(key) and await aiofile.is_file(key) and \
            await aiofile.get_mtime(key) != wrapper.timestamp
