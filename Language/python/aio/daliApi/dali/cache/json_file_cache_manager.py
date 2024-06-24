# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: json_file_cache_manager.py
@time: 2024/1/21  20:04
@desc: 
"""
import json

from dali.utils.log import Log
from dali.cache import CacheDataWrapper
from dali.cache.file_cache_manager import FileCacheManager


class JsonFileCacheManager(FileCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "JsonFileCacheManager":
        if JsonFileCacheManager.__instance is None:
            JsonFileCacheManager.__instance = JsonFileCacheManager()
        return JsonFileCacheManager.__instance

    async def wrap_data(self, key) -> CacheDataWrapper:
        wrapper = await super().wrap_data(key)
        if wrapper and wrapper.data:
            wrapper.data = json.loads(wrapper.data)
            Log().get_instance().debug(f"load json file {key}")
        return wrapper
