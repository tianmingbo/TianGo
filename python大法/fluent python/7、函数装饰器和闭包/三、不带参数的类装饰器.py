'''
基于类装饰器的实现，必须实现 __call__ 和 __init__两个内置函数。
__init__ ：接收被装饰函数
__call__ ：实现装饰逻辑。
'''


class logger(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("[INFO]: the function {func}() is running..." \
              .format(func=self.func.__name__))
        return self.func(*args, **kwargs)


@logger
def say(something):
    print("say {}!".format(something))


say("hello")
