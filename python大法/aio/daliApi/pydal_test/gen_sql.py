# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: gen_sql.py
@time: 2024/1/21  20:59
@desc: 
"""

from pydal import DAL, Field

if __name__ == '__main__':
    db = DAL("mysql://root:123456@150.158.47.35:23306/mydb")
    db.define_table(
        'student',
        Field('name', 'string', length=128, default=''),
        Field('age', 'integer', default=18),
    )
    sql = db.student._insert(name='dali', age='18')
    db.commit()
    print(sql)
