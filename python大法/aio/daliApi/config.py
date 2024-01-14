# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: config.py
@time: 2024/1/9  22:21
@desc: 
"""
import os

SERVER_NAME = 'dali'

SERVER_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR_NAME = 'app'
APP_ROOT = os.path.join(SERVER_ROOT, APP_DIR_NAME)

APP_NAME = 'dali'

LOG_LEVEL = 10

STATIC_FILES_ROOT = os.path.join(APP_ROOT, 'static')

GLOBAL_CHARSET = 'utf-8'
