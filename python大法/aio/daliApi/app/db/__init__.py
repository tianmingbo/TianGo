# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: __init__.py
@time: 2024/1/21  21:32
@desc: 
"""
from app.db.aioDal.dal import AsyncDAL
from pydal import Field


class Db:
    __instance = None

    @staticmethod
    async def get_instance() -> 'Db':
        if Db.__instance is None:
            Db.__instance = Db()
            await Db.__instance._async_init()
        return Db.__instance

    async def _async_init(self):
        self._async_pydal = await AsyncDAL.create('150.158.47.35', 'root', '123456', 'mydb', port=23306)
        self._async_pydal.define_table('user', Field('name', 'string', length=128, default=''),
                                       Field('age', 'integer', default=18), )

    @property
    def async_pydal(self):
        return self._async_pydal
