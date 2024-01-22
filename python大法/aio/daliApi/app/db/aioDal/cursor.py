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

    @property
    def description(self):
        """
        获取描述信息 ('id', 3, None, 11, 11, 0, False)
        'id': 字段名称，表示字段在数据库表中的标识符。
        3: 字段索引，在数据库中用于排序和查找的字段索引。
        None: 默认值，如果字段没有提供值，则使用该默认值。
        11: 字段的最大字符数或数字长度。对于字符串字段，这表示可以存储的最大字符数；对于数字字段，这表示数字的最大长度。
        11: 字段的显示长度。对于数字字段，它表示数字显示的总位数，包括小数点和小数位数；对于字符串字段，它是字符显示的总长度。
        0: 字段的小数位数。对于数值字段，它表示允许的小数位数。
        False: 是否允许字段为空。如果为True，则字段允许为空；如果为False，则字段不允许为空。
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
