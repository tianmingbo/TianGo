# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: page_cache_manager.py
@time: 2024/1/16  21:46
@desc:  页面缓存
"""
from datetime import datetime

from dali.cache import BaseCacheManager, CacheDataWrapper


class PageCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "PageCacheManager":
        if PageCacheManager.__instance is None:
            PageCacheManager.__instance = PageCacheManager()
        return PageCacheManager.__instance

    async def wrap_data(self, key) -> CacheDataWrapper:
        pass

    async def will_reload(self, wrapper: CacheDataWrapper, key: str) -> bool:
        return datetime.now().timestamp() > wrapper.timestamp
