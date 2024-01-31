# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: aiofile.py
@time: 2024/1/14  19:40
@desc: 异步操作文件
"""
import asyncio
import os.path


async def read_file(file_path):
    try:
        loop = asyncio.get_running_loop()
        with open(file_path, 'rb') as file:
            content = await loop.run_in_executor(None, file.read)
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def exists(file_path):
    """
    判断文件是否存在
    :param file_path:
    :return:
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, os.path.exists, file_path
    )


async def is_file(file_path):
    """
    判断指定的路径是否存在文件
    :param file_path:
    :return:
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, os.path.isfile, file_path
    )


async def get_mtime(file_path):
    """
    获取指定目录的文件的修改时间
    :param file_path:
    :return:
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, os.path.getmtime, file_path
    )
