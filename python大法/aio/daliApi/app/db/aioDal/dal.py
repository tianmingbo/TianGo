# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: dal.py
@time: 2024/1/21  21:16
@desc: 使用pydal的生成sql功能，使用aiomysql操作数据库
"""

from pydal import DAL
import aiomysql
from aiomysql.pool import Pool
from .connection import AsyncDalConnection


class AsyncDAL:
    def __init__(self):
        self._pydal = None
        self._aiomysql_conn_pool = None

    @staticmethod
    async def create(host, user, pwd, db, port, pool_max=10, echo=True) -> 'AsyncDAL':
        return await AsyncDAL().async_init(host, user, pwd, db, port, pool_max, echo)

    async def async_init(self, host, user, pwd, db, port, pool_max, echo) -> 'AsyncDAL':
        """

        :param host:
        :param user:
        :param pwd:
        :param db:
        :param port:
        :param pool_max: 最大连接数
        :param echo: 是否输出sql
        :return:
        """
        self._pydal = DAL(f"mysql://{user}:{pwd}@{host}:{port}/{db}",
                          migrate=False, migrate_enabled=False, bigint_id=True)
        self._aiomysql_conn_pool = await aiomysql.create_pool(0, pool_max, echo, host=host,
                                                              port=port, user=user,
                                                              password=pwd, db=db)
        return self

    @property
    def aiomysql_conn_pool(self) -> Pool:
        return self._aiomysql_conn_pool

    def close(self):
        self.aiomysql_conn_pool.close()

    async def wait_closed(self):
        await self.aiomysql_conn_pool.wait_closed()

    def terminate(self):
        """终止连接池"""
        self.aiomysql_conn_pool.terminate()

    async def acquire(self) -> AsyncDalConnection:
        """
        通过连接池获取一个连接上下文对象，并将其封装到AsyncDalConnection
        :return:
        """
        return AsyncDalConnection(self._pydal, self._aiomysql_conn_pool)

    async def release(self, conn: AsyncDalConnection):
        """
        释放一个连接对象
        :param conn:
        :return:
        """
        await self.aiomysql_conn_pool.release(conn.aiomysql_conn)

    def define_table(self, table_name, *fields, **kwargs):
        self._pydal.define_table(table_name, *fields, **kwargs)
