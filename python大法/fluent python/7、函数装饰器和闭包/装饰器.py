# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 10:34
# @Author  : tmb
import time
import functools

# def clock(func):
#     @functools.wraps(func)  # 使用 functools.wraps 装饰器把相关的属性从 func复制到 clocked 中。
#     def clocked(*args, **kwargs):
#         t0 = time.time()
#         result = func(*args, **kwargs)
#         elapsed = time.time() - t0
#         name = func.__name__
#         arg_lst = []
#         if args:
#             arg_lst.append(', '.join(repr(arg) for arg in args))
#         if kwargs:
#             pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
#             arg_lst.append(', '.join(pairs))
#         arg_str = ', '.join(arg_lst)
#         print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
#         return result
#
#     return clocked


# def clock(func):
#     def clocked(*args):  #
#         t0 = time.perf_counter()
#         result = func(*args)  # func是自由变量。调用原来的函数，记录结果
#         elapsed = time.perf_counter() - t0
#         name = func.__name__
#         arg_str = ', '.join(repr(arg) for arg in args)
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#
#     return clocked

# 带参数的装饰器
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*args):
            t0 = time.perf_counter()
            result = func(*args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            arg_str = ', '.join(repr(arg) for arg in args)
            print(fmt.format(**locals()))
            return result

        return clocked

    return decorate


@clock('{name}({args}) -> {result}')
def snooze(seconds):
    time.sleep(seconds)


@clock('{name}({args}) -> {result}')
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


def test2(n=1):
    time.sleep(0.1)
    return n + 2


if __name__ == '__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))
    # @clock('{name}({args}) -> {result}')同下
    test2 = clock('{name}({args}) -> {result}')(test2)
    test2(100)

'''
template:

def helper(func):
    count = 0

    def inner(*args):
        nonlocal count
        func(*args)
        count += 1
        print(count)
        return count

    return inner


@helper
def hello(tmp):
    print('hello-%d' % tmp)


if __name__ == '__main__':
    for i in range(10):
        hello(i)
'''
