# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 11:29
# @Author  : tmb

class logger:
    def __init__(self, level="INFO"):
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f'level:{self.level},func: {func.__name__}()')
            func(*args, **kwargs)

        return wrapper


@logger(level='WARNING')
def say(something):
    print('say', something)


if __name__ == '__main__':
    say('hello')
