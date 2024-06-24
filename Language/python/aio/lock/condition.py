import asyncio
from asyncio import Condition


async def do_work(cond: Condition):
    print("等待条件锁")
    async with cond:
        print("已获得锁，然后立即释放")
        # 等待事件触发，一旦成功，重新获取条件锁
        await cond.wait()
        print("再次获得条件锁，继续执行逻辑")
        await asyncio.sleep(1)
    # 退出 async with 语句块后，释放条件锁。
    print("工作结束，释放锁")


async def fire_event(cond: Condition):
    await asyncio.sleep(5)
    print("准备获取条件锁")
    async with cond:
        # 通知所有任务：事件已经发生
        cond.notify_all()
    print("通知完毕，释放锁")


async def main():
    cond = Condition()
    asyncio.create_task(fire_event(cond))
    await asyncio.gather(do_work(cond), do_work(cond))


asyncio.run(main())
"""
等待条件锁
已获得锁，然后立即释放
等待条件锁
已获得锁，然后立即释放
准备获取条件锁
通知完毕，释放锁
再次获得条件锁，继续执行逻辑
工作结束，释放锁
再次获得条件锁，继续执行逻辑
工作结束，释放锁
"""
