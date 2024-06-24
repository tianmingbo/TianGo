# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: session_cache_manager.py
@time: 2024/1/21  18:07
@desc: 实现session机制
"""

from datetime import datetime

from dali.cache import BaseCacheManager, CacheDataWrapper


class SessionCacheManager(BaseCacheManager):
    __instance = None

    @staticmethod
    def get_instance() -> "SessionCacheManager":
        if SessionCacheManager.__instance is None:
            SessionCacheManager.__instance = SessionCacheManager()
        return SessionCacheManager.__instance

    async def wrap_data(self, key) -> CacheDataWrapper:
        return CacheDataWrapper({}, datetime.now().timestamp())

    async def set_cur_user(self, session_id: bytes, user):
        """
        设置当前登录的用户
        :param session_id:
        :param user:
        :return:
        """
        session = await self.get_data(session_id)
        session['cur_user'] = user

    async def get_cur_user(self, session_id: bytes):
        """
        获取当前登录的用户
        :param session_id:
        :return:
        """
        session = await self.get_data(session_id)
        return session.get('cur_user')

    async def will_reload(self, wrapper: CacheDataWrapper, key: str) -> bool:
        return False
