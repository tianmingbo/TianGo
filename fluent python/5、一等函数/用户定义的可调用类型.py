# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 22:30
# @Author  : tmb
import random


class BingboCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingboCage')

    def __call__(self):  # 实现__call__方法，实例化可调用
        return self.pick()


if __name__ == '__main__':
    bingo = BingboCage(range(3))
    print(bingo.pick())
    print(bingo())
    print(dir(bingo))
