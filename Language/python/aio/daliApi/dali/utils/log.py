# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: log.py
@time: 2024/1/9  22:22
@desc: 日志工具
"""
import logging
import config


class Log:
    __instance = None

    @staticmethod
    def get_instance():
        if not Log.__instance:
            Log.__instance = Log()
        return Log.__instance

    def __init__(self) -> None:
        self._log = logging.getLogger(config.APP_NAME)
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(
            logging.Formatter(
                fmt='%(levelname)s|||%(name)s|||%(asctime)s|||%(pathname)s(line-%(lineno)s)|||%(message)s'
            )
        )
        if self._log.parent:
            self._log.parent.handlers = []
            self._log.parent.addHandler(log_handler)
        self._log.setLevel(config.LOG_LEVEL)
        self.info = self._log.info
        self.debug = self._log.debug
        self.warning = self._log.warning
        self.error = self._log.error
