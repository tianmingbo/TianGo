# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: cursor.py
@time: 2024/1/21  21:31
@desc: 
"""
from aiomysql.cursors import Cursor

from .query import AsyncQuery
from .table import Table


class AsyncCursor:
    def __init__(self, pydal, pydal_connection, aiomysql_cursor):
        self._pydal = pydal
        self._pydal_connection = pydal_connection
        self._aiomysql_cursor = aiomysql_cursor
        self._table_map = {}

    @property
    def aiomysql_cursor(self):
        return self._aiomysql_cursor

    @property
    def pydal_connection(self):
        return self._pydal_connection

    def description(self):
        """
        获取描述信息
        :return:
        """
        return self.aiomysql_cursor.description

    async def execute(self, sql, args=None):
        await self.aiomysql_cursor.execute(sql, args)

    async def execute_many(self, sql, args=None):
        await self.aiomysql_cursor.executemany(sql, args)

    async def fetchall(self):
        return await self.aiomysql_cursor.fetchall()

    async def fetchone(self):
        return await self.aiomysql_cursor.fetchone()

    async def fetchmany(self, size=1):
        return await self.aiomysql_cursor.fetchmany(size)

    async def close(self):
        await self.aiomysql_cursor.close()

    def lastrowid(self):
        return self.aiomysql_cursor.lastrowid

    def rowcount(self):
        """获取sql语句影响的行数"""
        return self.aiomysql_cursor.rowcount

    def __getattr__(self, item):
        pydal_table = self._pydal.__getattr__(item)
        if pydal_table in self._table_map:
            async_table = self._table_map[pydal_table]
        else:
            async_table = Table(self._pydal, self, pydal_table)
            self._table_map[pydal_table] = async_table
        return async_table

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __call__(self, *args, **kwargs) -> AsyncQuery:
        return AsyncQuery(self, self._pydal(*args))

