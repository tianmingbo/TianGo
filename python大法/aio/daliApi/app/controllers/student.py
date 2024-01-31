# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: student.py
@time: 2024/1/22  20:42
@desc: 
"""

from app.db import Db
from dali.http import Request, Response


async def index(req: Request, res: Response):
    db_manager = await Db.get_instance()
    conn = await db_manager.async_pydal.acquire()
    print(conn.autocommit_mode())
    db = await conn.cursor()
    students = await db(db.user.id > 0).select()
    await db.close()
    await db_manager.async_pydal.release(conn)
    print(students)
    await res.end(b'')
