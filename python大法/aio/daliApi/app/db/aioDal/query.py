# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: query.py
@time: 2024/1/21  21:32
@desc: 
"""
from . import row


class AsyncQuery:
    def __init__(self, pydal_cursor, dal_query):
        self._pydal_cursor = pydal_cursor
        self._dal_query = dal_query

    def _select(self, *args, **kwargs):
        return self._dal_query._select(*args, **kwargs)

    async def select(self, *args, **kwargs):
        sql: str = self._select(*args, **kwargs)
        sql = sql.replace('\\', '')
        print(sql)
        await self._pydal_cursor.execute(sql)
        res = await self._pydal_cursor.fetchall()
        return row.Rows(self._pydal_cursor.description, res)

    def _update(self, **kwargs):
        return self._dal_query._update(**kwargs)

    async def update(self, **kwargs):
        sql: str = self._update(**kwargs)
        sql = sql.replace('\\', '')
        print(sql)
        await self._pydal_cursor.execute(sql)
        return await self._pydal_cursor.rowcount

    def _delete(self):
        return self._dal_query._delete()

    async def delete(self):
        sql: str = self._delete()
        sql = sql.replace('\\', '')
        print(sql)
        await self._pydal_cursor.execute(sql)
        return await self._pydal_cursor.rowcount

    def _count(self):
        return self._dal_query._count()

    async def count(self):
        sql: str = self._count()
        sql = sql.replace('\\', '')
        print(sql)
        await self._pydal_cursor.execute(sql)
        return await self._pydal_cursor.fetchone()[0]

    async def isempty(self):
        return await self.count() == 0
