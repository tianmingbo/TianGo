from functools import partial


# 偏函数partial  它的作用是可以存储参数


def func(a=0, b=0, c=0, d=0):
    print(a, b, c, d)
    return a + b + c + d


# 第一个参数是函数的对象，第二个以及后面的参数都是函数的参数，这里严格按照python的传传参规则
res = partial(func, 1)
print(res(2, 3))
