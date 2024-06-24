# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: modules_cache_manager.py
@time: 2024/1/15  22:06
@desc: 实现导入和重新加载模块功能,实现热更新
"""
import importlib
import os.path

import config
from dali.utils.log import Log
from dali.cache.base_cache_manager import BaseCacheManager, CacheDataWrapper
from dali.utils import aiofile


class ModulesCacheManager(BaseCacheManager):
    __instance = None
    log = Log.get_instance()

    @staticmethod
    def get_instance() -> "ModulesCacheManager":
        if ModulesCacheManager.__instance is None:
            ModulesCacheManager.__instance = ModulesCacheManager()
        return ModulesCacheManager.__instance

    @staticmethod
    def file_name_from_module_name(module_name: str) -> str:
        """
        将模块名转为文件路径
        :param module_name:
        :return:
        """
        file_path = module_name.split('.')
        return os.path.join(config.SERVER_ROOT,
                            file_path[0],
                            file_path[1],
                            f'{file_path[2]}.py')

    async def wrap_data(self, key) -> CacheDataWrapper:
        m, t = None, 0
        try:
            # 导入模块
            m = importlib.import_module(key)
            m_file = self.file_name_from_module_name(key)
            t = await aiofile.get_mtime(m_file)
        except ModuleNotFoundError:
            self.log.warning(f"module {key} not found")
        return CacheDataWrapper(m, t) if m else None

    async def will_reload(self, wrapper: CacheDataWrapper, key: str) -> bool:
        return_value = False
        if key in self.cache_map:
            m_file = self.file_name_from_module_name(key)
            # 如果已缓存的文件时间戳和现有文件的时间戳不一致，则重新加载模块
            if await aiofile.exists(m_file) and \
                    await aiofile.is_file(m_file) and \
                    (await aiofile.get_mtime(m_file)) != wrapper.timestamp:
                importlib.reload(wrapper.data)
                return_value = True
        else:
            return_value = True
        return return_value
