# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 17:48
# @Author  : tmb
class MaxQueue:

    def __init__(self):
        self.queue = []
        self.aide = []

    def max_value(self) -> int:
        if not self.queue:
            return -1
        return self.aide[-1]

    def push_back(self, value: int) -> None:
        self.queue.append(value)
        if not self.aide or value > self.aide[-1]:
            self.aide.append(value)

    def pop_front(self) -> int:
        if not self.queue:
            return -1
        tmp = self.queue.pop(0)
        if self.aide[-1] == tmp:
            self.aide.pop()
        return tmp


if __name__ == '__main__':
    obj = MaxQueue()
    param_1 = obj.max_value()
    obj.push_back(1)
    obj.push_back(2)
    param_3 = obj.pop_front()
    param_4 = obj.max_value()
    print(param_1, param_3, param_4)
