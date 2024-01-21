# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: config.py
@time: 2024/1/9  22:21
@desc: 
"""
import os

SERVER_NAME = 'dali'

LANGUAGE = None

SERVER_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR_NAME = 'app'
APP_ROOT = os.path.join(SERVER_ROOT, APP_DIR_NAME)

LANGUAGE_DIR_NAME = "languages"
LANGUAGE_ROOT = os.path.join(APP_ROOT, LANGUAGE_DIR_NAME)

APP_NAME = 'dali'

LOG_LEVEL = 10

STATIC_FILES_ROOT = os.path.join(APP_ROOT, 'static')

GLOBAL_CHARSET = 'utf-8'

CONTROLLERS_DIR_NAME = 'controllers'
# 控制器所在目录
CONTROLLERS_ROOT = os.path.join(APP_ROOT, CONTROLLERS_DIR_NAME)
DEFAULT_CONTROLLER = 'default'
DEFAULT_ACTION = 'index'
SESSION_ID_KEY = 'session_id'
