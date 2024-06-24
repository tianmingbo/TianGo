"""
yield from
主要作用是打开双向通道，把最外层的调用方和最内层的子生成器连接起来，这样二者可以直接发送和产出值，
还可以直接传入异常，而不用在位于中间的协程添加大量处理异常的样板代码。


委派生成器
  包含yield from <iterable> 表达式的生成器函数
子生成器
  从yield from表达式中<iterable> 部分获取的生成器
调用方
  调用委派生成器的客户端代码

*******
一个委派生成器使用yield from调用一个子生成器，而那个子生成器也是委派生成器，也可以使用yield from调用另一个子生成器，以此类推。
最终，这个链条要以一个只使用yield表达式的简单生成器结束（也可以使用任何可迭代的对象结束）
"""
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# 子生成器
def average():
    count = 0
    num = 0
    res = None
    while True:
        cur_num = yield
        if cur_num is None:
            break  # 退出条件
        count += cur_num
        num += 1
        res = count / num
    return Result(num, res)


# 委派生成器
def grouper(result, key):
    # 每次迭代时都会创建一个average实例；每个实例都是作为协程使用的生成器对象
    while True:
        # 在yield from表达式处暂停，调用方直接把数据发给子生成器，子生成器再把产出的值发给调用方。子生成器返回之后，解释器抛出StopIteration，
        # 并把返回值附加到异常对象上，此时委派生成器恢复。
        # 然后把返回的值绑定到result[key]上
        result[key] = yield from average()


# 客户端（调用方）
def main(data):
    result = {}
    for key, values in data.items():
        group = grouper(result, key)
        next(group)  # 预激
        for value in values:
            # 把各个value传给grouper。传入的值最终到达cur_num = yield这一行。grouper不知道传入的值是什么（这就是建立了一个通道）
            group.send(value)
        group.send(None)  # 退出
    print(result)


if __name__ == '__main__':
    data = {
        'girls': [1, 3, 45, 34, 23, 23],
        'boys': [67, 56, 434, 6346, 346, 364]
    }
    main(data)
