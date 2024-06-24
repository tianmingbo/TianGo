from abc import ABCMeta, abstractmethod


# 处理者
class Handler(metaclass=ABCMeta):
    def __init__(self, next_handler=None):
        self.__next_handler = next_handler  # 后续处理者,下一个责任人

    def get_next_handler(self):
        return self.__next_handler

    @abstractmethod
    def handle(self, request):
        pass


# 具体处理者
class ConcreteHandler1(Handler):

    def handle(self, request):
        if 条件成立:  # 判断是否可以处理
            处理并返回结果
        else:  # 如果自己不能处理，则交给后面的处理者处理
            self.get_next_handler().handle(request)


class ConcreteHandler2(Handler):
    def handle(self, request):
        if 条件成立:
            处理并返回结果
        else:
            self.get_next_handler().handle(request)


class Request:
    def __init__(self, name, day_off):
        self.__name = name
        self.__day_off = day_off

    def get_name(self):
        return self.__name

    def get_day_off(self):
        return self.__day_off


if __name__ == '__main__':
    handler1 = ConcreteHandler1()
    handler2 = ConcreteHandler2(handler1)
    req = Request('t', 3)
    res = handler2.handle(req)
