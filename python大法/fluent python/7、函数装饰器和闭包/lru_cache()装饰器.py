# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:39
# @Author  : tmb
import functools
from 装饰器 import clock


@functools.lru_cache()  # ➊
@clock  # ➋
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == '__main__':
    print(fibonacci(6))
