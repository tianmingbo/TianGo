"""
gen.throw()

使生成器在暂停的yield表达式处抛出指定的异常。
如果生成器处理了异常，代码会向下执行到下一个yield表达式，而产出的值会成为调用gen.throw方法得到的返回值。
如果没有处理异常，那会向上冒泡，传给调用方

gen.close()

使生成器在暂停的yield表达式处抛出GeneratorExit异常。
"""


class DemoException(Exception):
    pass


def exc_handling():
    print('coroutine started')
    try:
        while True:
            try:
                x = yield 10
            except DemoException:
                print("*** DemoException handled, Continuing...")
            else:
                print(f"-> coroutine received: {x}")
    finally:
        print('coroutine ended')


if __name__ == '__main__':
    gen = exc_handling()
    gen.send(None)
    gen.send(11)
    print(gen.throw(DemoException))  # 会继续运行
    gen.send(12)
    gen.close()
