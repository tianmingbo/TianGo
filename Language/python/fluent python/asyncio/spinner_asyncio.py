import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/+\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():
    yield from asyncio.sleep(3)  # 把控制器交给主循环，休眠结束后恢复这个协程
    return 33


@asyncio.coroutine
def supervisor():
    spinner = asyncio.Task(spin("thinking"))  # asyncio.Task基本与threading.Thread等效
    # spinner = asyncio.ensure_future(spin("thinking"))
    print('spinner object', spinner)
    result = yield from slow_function()
    spinner.cancel()
    return result


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
