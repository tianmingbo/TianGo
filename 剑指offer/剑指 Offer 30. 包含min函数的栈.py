class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.stack2 = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.stack2 or self.stack2[-1] > x:
            self.stack2.append(x)

    def pop(self) -> None:
        if self.stack.pop() == self.stack2[-1]:
            self.stack2.pop()

    def top(self) -> int:
        return self.stack[-1]

    def min(self) -> int:
        return self.stack2[-1]


# Your MinStack object will be instantiated and called as such:
obj = MinStack()
obj.push(1)
# obj.pop()
param_3 = obj.top()
param_4 = obj.min()
print(param_3, param_4)
