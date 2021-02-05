# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 20:45
# @Author  : tmb
class CQueue:

    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def appendTail(self, value: int) -> None:
        # 1 -> 2
        while self.stack1:
            self.stack2.append(self.stack1.pop())
        # add value
        self.stack1.append(value)
        while self.stack2:
            self.stack1.append(self.stack2.pop())

    def deleteHead(self) -> int:
        if not self.stack1:
            return -1
        return self.stack1.pop()

# Your CQueue object will be instantiated and called as such:
# obj = CQueue()
# obj.appendTail(value)
# param_2 = obj.deleteHead()
