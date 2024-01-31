# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: connection.py
@time: 2024/1/21  21:31
@desc: 
"""

from aiomysql.connection import Connection

from .cursor import AsyncCursor


class AsyncDalConnection:
    def __init__(self, pydal, aiomysql_conn: Connection):
        self._pydal = pydal
        self._aiomysql_conn = aiomysql_conn

    @property
    def aiomysql_conn(self) -> Connection:
        return self._aiomysql_conn

    async def commit(self):
        """提交数据"""
        await self.aiomysql_conn.commit()

    async def rollback(self):
        """回滚"""
        await self.aiomysql_conn.rollback()

    def close(self):
        self.aiomysql_conn.close()

    async def autocommit(self, mode: bool):
        """
        自动提交？
        :param mode:
        :return:
        """
        await self.aiomysql_conn.autocommit(mode)

    def autocommit_mode(self):
        return self.aiomysql_conn.autocommit_mode

    async def cursor(self) -> AsyncCursor:
        return AsyncCursor(self._pydal, self, await self.aiomysql_conn.cursor())
