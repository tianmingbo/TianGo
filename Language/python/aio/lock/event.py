import asyncio
from asyncio import Event


def trigger_event(event: Event):
    event.set()


async def do_work_on_event(event: Event):
    print("等待事件发生")
    await event.wait()  # 如果标志位不为 True，那么此处会阻塞
    # 一旦事件发生，wait 将不再阻塞，我们可以继续运行程序
    print("event 标志位被设置为 True，开始执行逻辑")
    await asyncio.sleep(1)
    print("执行结束")
    # 重置事件，后续 await event.wait() 会再次阻塞
    event.clear()


async def main():
    # Event 实例化之后，标志位默认为 False
    event = asyncio.Event()
    # 5 秒后调用 trigger_event，在里面会执行 event.set()
    asyncio.get_running_loop().call_later(5, trigger_event, event)
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))


asyncio.run(main())
"""
等待事件发生
等待事件发生
event 标志位被设置为 True，开始执行逻辑
event 标志位被设置为 True，开始执行逻辑
执行结束
执行结束
"""
