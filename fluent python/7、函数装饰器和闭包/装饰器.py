# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 10:34
# @Author  : tmb
import time
import functools


def clock(func):
    @functools.wraps(func)  # 使用 functools.wraps 装饰器把相关的属性从 func复制到 clocked 中。
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result

    return clocked


# def clock(func):
#     def clocked(*args):  # ➊
#         t0 = time.perf_counter()
#         result = func(*args)  # ➋
#         elapsed = time.perf_counter() - t0
#         name = func.__name__
#         arg_str = ', '.join(repr(arg) for arg in args)
#         print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#         return result
#
#     return clocked


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == '__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))

'''
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
