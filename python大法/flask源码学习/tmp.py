class Number:
    def __init__(self, value):
        self.value = value

    def __rlshift__(self, other):
        print(other)
        if isinstance(other, int):
            return self.value << other
        return NotImplemented


# 创建一个 Number 对象
num = Number(5)

# 演示右操作数左移位运算
result1 = 10 << num
print(result1)  # 输出: 320

result2 = 2.5 << num
print(result2)  # 输出: NotImplemented