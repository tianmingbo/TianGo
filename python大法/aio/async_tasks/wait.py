import asyncio


async def delay(seconds):
    await asyncio.sleep(seconds)
    if seconds == 4:
        raise ValueError("sleep 4 error")
    print(f"我睡了 {seconds} 秒")


async def main():
    tasks = [asyncio.create_task(delay(seconds)) for seconds in range(10)]
    # 和 gather 一样，默认会等待所有任务都完成,支持设置timeout, 当出现第一个异常时退出
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    print(f"已完成的任务数: {len(done)}")
    print(f"未完成的任务数: {len(pending)}")

    for done_task in done:
        # 这里不能使用 await done_task，因为当任务完成时，它就等价于 done_task.result()
        # 而任务出现异常时，调用 result() 是会将异常抛出来的，所以我们需要先检测异常是否为空
        # print(await done_task)
        exception = done_task.exception()
        if exception:
            print(exception)
        else:
            print(done_task.result())
    # 此时未完成的任务仍然在后台运行
    for t in pending:
        print(t.get_name())
        t.cancel()  # 取消任务
    await asyncio.sleep(8)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""
已完成的任务数: 3
未完成的任务数: 0
我睡了 2 秒
我睡了 4 秒
我睡了 3 秒
"""
