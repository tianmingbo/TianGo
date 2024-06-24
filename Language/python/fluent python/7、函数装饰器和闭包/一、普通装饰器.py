# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 9:45
# @Author  : tmb

def logger(func):
    def inner(*args, **kwargs):
        print(f'start running {func.__name__}')
        func(*args, **kwargs)
        print('over')

    return inner


# @logger
def add(x, y):
    print(f'{x}+{y} ={x + y}')


if __name__ == '__main__':
    add = logger(add)  # 同@logger ，实际作用是 addf=inner 函数
    add(1, 2)
