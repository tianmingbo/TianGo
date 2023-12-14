"""
在请求完成时立即处理
"""
import asyncio

from util.py.async_timed import async_timed


async def delay(second: int):
    await asyncio.sleep(second)
    if second == 4:
        raise ValueError("sleep 4 error!!")
    return f"sleep {second}"


@async_timed
async def main():
    tasks = [asyncio.create_task(delay(i)) for i in [5, 4, 2, 7, 1, 9]]
    # 不用等待每一个任务都完成，哪个先完成，哪个就被迭代
    for finished_task in asyncio.as_completed(tasks, timeout=5):
        try:
            print(await finished_task)
        except Exception as e:
            print(e)
    # 虽然会抛出异常，但是任务还在后台继续执行
    print(tasks[1].done())
    print(tasks[2].done())
    print(tasks[3].done())  # False
    print(tasks[4].done())


"""
协程 main 开始执行
sleep 1
sleep 2
sleep 4
sleep 5
sleep 7
sleep 9
协程 main 用 9.000927027000001 秒执行完毕
"""

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
