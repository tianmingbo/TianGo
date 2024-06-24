import asyncio


async def execute(x):
    print('number:', x)


coroutine = execute(1)  # 调用execute方法，并不会执行，而是返回一个协程对象
print('coroutine', coroutine)
loop = asyncio.get_event_loop()  # 创建一个事件循环loop
# task = asyncio.ensure_future(coroutine) # 定义task的另一种方式
task = loop.create_task(coroutine)  # task是协程的进一步封装，多了状态
print('front', task)
loop.run_until_complete(task)
print('end', task)
