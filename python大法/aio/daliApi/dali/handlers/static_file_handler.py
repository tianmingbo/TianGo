# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: static_file_handler.py
@time: 2024/1/10  22:44
@desc: 静态文件处理
"""
import config
from dali.utils import aiofile

mime_type_map = {
    '.txt': b'text/plain',
    '.html': b'text/html',
    '.json': b'application/json',
    '.jpeg': b'image/jpeg',
    '.jpg': b'image/jpeg',
    '.png': b'image/png',
    '.gif': b'image/gif',
    '.mp3': b'audio/mpeg',
    '.wav': b'audio/wav',
    '.mp4': b'video/mp4',
    '.mov': b'video/quicktime',
    '.pdf': b'application/pdf',
    '.js': b'application/javascript'
    # 添加其他常见的后缀和 MIME 类型
}


def get_mime_type(file_path: str) -> bytes:
    """
    根据文件路径获取相应的mime_type
    :param file_path:
    :return:
    """
    mime_type = b'text/plain'
    last_dot_index = file_path.rfind('.')
    if last_dot_index > -1:
        file_type = file_path[last_dot_index:]
        if file_type in mime_type_map:
            mime_type = mime_type_map[file_type]
    return mime_type


async def handle_static_file_request(scope, send) -> bool:
    """
    处理静态文件请求
    :param scope:
    :param send:
    :return: 如果文件存在并且已经发送，则返回True
    """
    if scope['method'] != 'GET':
        return False
    data_sent = False

    file_path = f"{config.STATIC_FILES_ROOT}{scope['path']}"
    file_content = None
    # 如果该路径存在并是个文件
    if await aiofile.exists(file_path) and await aiofile.is_file(file_path):
        file_content = await aiofile.read_file(file_path)
    if file_content:
        mime_type = get_mime_type(file_path)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', mime_type],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': file_content,
            'more_body': False
        })
        data_sent = True
    return data_sent
