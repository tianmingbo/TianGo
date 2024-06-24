import asyncio


async def execute(x):
    """
    async定义的方法变成了一个无法直接执行的协程对象，必须将此对象注册到事件循环中才行
    :param x:
    :return:
    """
    print('number:', x)


coroutine = execute(1)  # 调用execute方法，并不会执行，而是返回一个协程对象
print('coroutine', coroutine)
loop = asyncio.get_event_loop()  # 创建一个事件循环loop
loop.run_until_complete(coroutine)  # 将协程对象注册到事件循环中，并启动


