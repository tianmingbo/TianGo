# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: static_file_handler.py
@time: 2024/1/10  22:44
@desc: 静态文件处理
"""
import config
from dali.utils import aiofile
from dali.utils.http_helper import timestamp_to_http_time

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
    # 如果该路径存在并是个文件
    if await aiofile.exists(file_path) and await aiofile.is_file(file_path):
        file_content = await aiofile.read_file(file_path)
        file_last_modify = await aiofile.get_mtime(file_path)
        file_last_modify_http_str = timestamp_to_http_time(file_last_modify)
        mime_type = get_mime_type(file_path)

        headers = scope['headers']
        if_modified_since = b''
        if headers and len(headers):
            for h in headers:
                if len(h) >= 2:
                    hk, hv = h[0], h[1]
                    if hk == b'if-modified-since':
                        if_modified_since = hv
                        break

        if if_modified_since:
            # 如果客户端的 If-Modified-Since 头与服务器的 Last-Modified 头相同，服务器可以返回 304 Not Modified。
            if if_modified_since == file_last_modify_http_str:
                await send({
                    'type': 'http.response.start',
                    'status': 304,
                    'headers': [
                        [b'content-type', mime_type],
                        [b'last-modified', file_last_modify_http_str]
                    ]
                })
                await send({
                    'type': 'http.response.body',
                    'body': b'',
                    'more_body': False
                })
                data_sent = True
        if not data_sent:
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', mime_type],
                    [b'last-modified', file_last_modify_http_str]
                ]
            })
            await send({
                'type': 'http.response.body',
                'body': file_content,
                'more_body': False
            })
            data_sent = True
    return data_sent
