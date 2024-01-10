# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: static_file_handler.py
@time: 2024/1/10  22:44
@desc: 静态文件处理
"""
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
