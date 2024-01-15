# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: base_cache_manager.py
@time: 2024/1/15  21:16
@desc: 缓存类
"""

from abc import ABCMeta, abstractmethod


class CacheDataWrapper:
    """
    用于包装缓存的数据
    """

    def __init__(self, data, timestamp) -> None:
        # 记录数据缓存的时间戳
        self.timestamp = timestamp
        # 记录缓存的数据
        self.data = data


class BaseCacheManager(metaclass=ABCMeta):
    """
    缓存管理器抽象基类，仅实现缓存管理功能
    """

    def __init__(self):
        self._cache_map = {}  # 缓存数据
        self._wrap_data_callback = None  # 数据包装函数
        self._will_reload_callback = None  # 实现确定何时重新缓存数据的回调函数

    @abstractmethod
    async def wrap_data(self, key) -> CacheDataWrapper:
        pass

    async def retrieve_cache_data(self, key):
        if not self._wrap_data_callback:
            self._wrap_data_callback = self.wrap_data
        wrapper = await self._wrap_data_callback(key)
        if wrapper:
            self._cache_map[key] = wrapper
        return wrapper.data if wrapper else None

    async def get_data(self, key,
                       wrap_data_callback=None,
                       will_reload_callback=None):
        """
        获取数据，该函数将自动根据需要创建新数据或返回缓存的数据
        :param key: 缓存键
        :param wrap_data_callback: 包装数据的回调函数，置空将调用默认的 wrap_data 函数以创建数据
        :param will_reload_callback: 提示是否创建新数据的回调函数，置空将使用self.will_reload进行回调
        :return:
        """
        self._wrap_data_callback = wrap_data_callback or self.wrap_data
        self._will_reload_callback = will_reload_callback or self.will_reload
        if key in self._cache_map:
            wrapper: CacheDataWrapper = self._cache_map[key]
            result = wrapper.data
            if await self._will_reload_callback(wrapper, key):
                result = await self.retrieve_cache_data(key)
        else:
            result = await self.retrieve_cache_data(key)
        return result

    @abstractmethod
    async def will_reload(self, wrapper: CacheDataWrapper, key: str) -> bool:
        """
        是否需要重新加载数据
        :param wrapper:
        :param key:
        :return:
        """
        pass

    def clear(self):
        self._cache_map.clear()

    @property
    def cache_map(self):
        return self._cache_map
