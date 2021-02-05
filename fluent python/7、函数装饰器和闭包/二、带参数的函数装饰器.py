# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 10:47
# @Author  : tmb
def say_hello(country):
    def wrapper(func):
        def deco(*args, **kwargs):
            if country == 'china':
                print('你好')
            elif country == 'america':
                print('hello')
            func(*args, **kwargs)

        return deco

    return wrapper


# @say_hello('china')
def xiaoming():
    pass


@say_hello("america")
def jackie():
    pass


if __name__ == '__main__':
    xiaoming = say_hello('china')(xiaoming)
    xiaoming()
    jackie()
