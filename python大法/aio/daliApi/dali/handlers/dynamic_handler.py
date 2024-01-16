# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: dynamic_handler.py
@time: 2024/1/15  20:17
@desc:  将请求路径分为控制器和动作进行处理。如/user/list对应的控制器为user，动作为list
"""
import importlib
import inspect
import os

import config
from dali import http
from dali.cache import ModulesCacheManager
from dali.utils import aiofile


async def handle_dynamic_request(scope, receive, send):
    data_sent = False
    request_path = scope['path']
    tokens = request_path.split('/')
    tokens_len = len(tokens)
    controllers_name = config.DEFAULT_CONTROLLER
    if tokens_len > 1:
        controllers_name = tokens[1] or config.DEFAULT_CONTROLLER
    action_name = config.DEFAULT_ACTION
    if tokens_len > 2:
        action_name = tokens[2] or config.DEFAULT_ACTION
    controller_file = os.path.join(config.CONTROLLERS_ROOT, controllers_name + '.py')
    # 如果该控制器存在，尝试导入该文件
    if await aiofile.exists(controller_file):
        # 热更新
        controller_obj = await ModulesCacheManager.get_instance().get_data(
            f"{config.APP_DIR_NAME}.{config.CONTROLLERS_DIR_NAME}.{controllers_name}"
        )
        if controller_obj:
            action = getattr(controller_obj, action_name, None)
            if action:
                req = http.Request(scope, receive)
                res = http.Response(req, send)
                req.controller = controllers_name
                req.action = action

                req.args = tokens[3:] if len(tokens) > 3 else []
                # 如果是类，先实例化再执行
                if inspect.isclass(action):
                    await action()(req, res)
                else:
                    await action(req, res)
                data_sent = res.body_sent
        return data_sent
