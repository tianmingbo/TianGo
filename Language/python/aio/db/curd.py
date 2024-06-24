import asyncio

from sqlalchemy import text, Table, MetaData, Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from conn import DBConnectionManager, engine

table = Table(
    "girls",  # 表名
    MetaData(),  # MetaData() 实例
    # 表里面的列
    Column("id", INTEGER, primary_key=True, autoincrement=True),
    Column("name", VARCHAR),
    Column("age", INTEGER),
    Column("address", VARCHAR)
)


async def insert():
    async with engine.connect() as conn:
        query = table.insert().values(
            [{"name": "八意永琳", "age": 20, "address": "永远亭"},
             {"name": "十六夜咲夜", "age": 33, "address": "红魔乡"}])
        result = await conn.execute(query)
        # 返回受影响的行数
        print(result.rowcount)  # 1
        # 返回数据在插入之后的主键
        print(result.inserted_primary_key)  # (5,)
        # 对于增删改而言，还必须调用一次 commit
        # 否则数据不会写入到库中
        await conn.commit()


async def remove():
    async with engine.connect() as conn:
        query = table.delete().where(table.c.id == 1)
        res = await conn.execute(query)
        print(res.rowcount)
        await conn.commit()


async def update():
    async with engine.connect() as conn:
        query = table.update().where(table.c.id == 1).values({"name": "dali"})
        result = await conn.execute(query)
        print(result.rowcount)  # 受影响的行数
        await conn.commit()


class Select:
    @staticmethod
    async def get_data2():
        async with engine.connect() as session:
            # :id 就是一个占位符，那么它等于多少呢？
            # 再调用 bindparams 指定即可
            # 并且占位符的数量没有限制
            query = text("SELECT * FROM girls WHERE id = :id").bindparams(id=1)
            result = await session.execute(query)
        data = result.fetchall()
        # 此时只返回了两条数据
        print([dict(zip(result.keys(), d)) for d in data])
        """
        [{'id': 2, 'name': '古明地恋', 'age': 16, 'address': '地灵殿'}, 
         {'id': 3, 'name': '雾雨魔理沙', 'age': 19, 'address': '魔法森林'}, 
         {'id': 4, 'name': '琪露诺', 'age': 60, 'address': '雾之湖'}]
        """
        print('\n')

    # 需要定义一个协程函数
    @staticmethod
    async def get_data():
        # 引擎内部维护了一个连接池，engine.connect() 会从池子里取出一个连接
        async with engine.connect() as session:
            # 调用 conn.execute() 执行 SQL 语句，SQL 语句需要传到 text 方法中
            query = text("SELECT * FROM girls")
            result = await session.execute(query)

        # 返回的 result 是一个 CursorResult 对象，通过 keys 方法可以拿到选择的字段
        columns = result.keys()
        print(columns)
        """
        RMKeyView(['id', 'name', 'age', 'address'])
        """
        # 调用 result.fetchone() 拿到单条数据
        data = result.fetchone()
        print(data)
        """
        (1, '古明地觉', 17, '地灵殿')
        """
        # 虽然显示的是一个元组，但它其实是一个 Row 对象，不过可以当成元组来用
        # 我们将它转成字典
        print(dict(zip(columns, data)))
        """
        {'id': 1, 'name': '古明地觉', 'age': 17, 'address': '地灵殿'}
        """

        # result 内部有一个游标
        # 再调用 result.fetchone() 会返回下一条数据
        print(result.fetchone())
        print(result.fetchone())
        print(result.fetchone())
        """
        (2, '古明地恋', 16, '地灵殿')
        (3, '雾雨魔理沙', 19, '魔法森林')
        (4, '琪露诺', 60, '雾之湖')
        """
        # 库里面总共就 4 条数据
        # 所以当没有数据时，就会返回 None
        print(result.fetchone())
        """
        None
        """
        print('\n')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(remove())
