import asyncio

from sqlalchemy import text

from db.conn import DBConnectionManager

db = DBConnectionManager(password="westwell")


class Add:
    pass


class Remove:
    pass


class Update:
    pass


class Select:
    @staticmethod
    async def get_data2():
        async with db.session() as session:
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
        session = db.session()
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
    loop.run_until_complete(Select.get_data())
