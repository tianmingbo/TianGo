# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: action_with_db.py
@time: 2024/1/22  21:40
@desc: 
"""
from app.db import Db
from dali.utils.log import Log


class ActionWithDb:
    async def execute(self, req, res):
        raise NotImplementedError()

    async def __call__(self, *args, **kwargs):
        db_manager = await Db.get_instance()
        conn = await db_manager.async_pydal.acquire()
        # 数据库对象，用于操作数据库
        self.db = await conn.cursor()
        err = None
        try:
            await self.execute(*args, **kwargs)
            await conn.commit()
        except BaseException as e:
            err = e
            Log().get_instance().error(e)
            await conn.rollback()
        await self.db.close()
        # 释放连接
        await db_manager.async_pydal.release(conn)
        if err:
            raise err
