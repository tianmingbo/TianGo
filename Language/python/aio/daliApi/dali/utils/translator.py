# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: translator.py
@time: 2024/1/21  20:07
@desc: 翻译工具，加载和翻译文字
"""
import os

import config
from dali.cache.json_file_cache_manager import JsonFileCacheManager
from dali.utils import aiofile


async def get_language_dict(language: str):
    """
    根据对应的语言，获取对应的字典
    :param language:
    :return:
    """
    language_dict = None
    language_file = os.path.join(config.LANGUAGE_ROOT, f'{language}.json')
    if await aiofile.exists(language_file) and await aiofile.is_file(language_file):
        language_dict = await JsonFileCacheManager.get_instance().get_data(language_file)
    return language_dict


async def translate(words: str, target_language: str) -> str:
    """
    将指定的words翻译为目标语言
    :param words:
    :param target_language:
    :return:
    """
    result = words
    language_dict = await get_language_dict(target_language)
    if language_dict and words in language_dict:
        result = language_dict[words]
    return result
