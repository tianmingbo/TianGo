# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 22:41
# @Author  : tmb
s = 'ABC'
it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:  # 迭代器到头了
        del it
        break
'''
标准的迭代器接口有两个方法。
__next__
返回下一个可用的元素，如果没有元素了，抛出 StopIteration 异常。
__iter__
返回 self，以便在应该使用可迭代对象的地方使用迭代器，例如在 for 循环中。
'''

'''
迭代器
迭代器是这样的对象：实现了无参数的 __next__ 方法，返回序列中的下一个元素；如
果没有元素了，那么抛出 StopIteration 异常。 Python 中的迭代器还实现了 __iter__ 方
法，因此迭代器也可以迭代。
'''
