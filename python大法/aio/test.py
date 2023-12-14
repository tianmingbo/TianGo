import asyncio
import aiomysql.sa
from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

# 定义一个数据库表
your_table = Table(
    'orm', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('age', Integer)
)


async def main():
    # 建立到数据库的异步连接
    engine = await aiomysql.sa.create_engine(
        user='root',
        db='test',
        host='127.0.0.1',
        password='123456'
    )

    # 插入数据
    async with engine.acquire() as conn:
        await conn.execute(your_table.insert().values(column1='abc', column2=123))

    # 查询数据
    async with engine.acquire() as conn:
        result = await conn.execute(your_table.select().where(your_table.c.column1 == 'abc'))
        rows = await result.fetchall()
        for row in rows:
            print(row)

    # 关闭连接
    engine.close()
    await engine.wait_closed()


# 运行主程序
asyncio.run(main())
