"""
请假审批->主管->部门总监->CEO->行政
根据请假天数,不同角色审批
"""

from abc import ABCMeta, abstractmethod


class Request:
    def __init__(self, name, day_off, reason):
        self.__name = name
        self.__day_off = day_off
        self.__reason = reason

    def get_name(self):
        return self.__name

    def get_day_off(self):
        return self.__day_off

    def get_reason(self):
        return self.__reason


class Handle(metaclass=ABCMeta):
    def __init__(self, name, title, next_handler=None):
        self.__name = name
        self.__title = title
        self.__next_handler = next_handler

    def get_name(self):
        return self.__name

    def get_title(self):
        return self.__title

    def get_next_handler(self):
        return self.__next_handler

    @abstractmethod
    def handle(self, request):
        pass


class Supervisor(Handle):

    def handle(self, request):
        if request.get_day_off() <= 2:
            print(f'{self.get_name()}批准{request.get_name()}请假{request.get_day_off()}')
        else:
            self.get_next_handler().handle(request)


class DepartManager(Handle):

    def handle(self, request):
        if 2 < request.get_day_off() <= 5:
            print(f'{self.get_name()}批准{request.get_name()}请假{request.get_day_off()}')
        else:
            self.get_next_handler().handle(request)


class CEO(Handle):

    def handle(self, request):
        if 5 < request.get_day_off() <= 10:
            print(f'{self.get_name()}批准{request.get_name()}请假{request.get_day_off()}')
        else:
            self.get_next_handler().handle(request)


class Administrator(Handle):

    def handle(self, request):
        if request.get_day_off() > 10:
            print(f'{self.get_name()}批准{request.get_name()}请假{request.get_day_off()}')
        else:
            self.get_next_handler().handle(request)


if __name__ == '__main__':
    req = Request('dali', 50, "null")
    d = Administrator('rl', 'ad')
    c = CEO('we', 'ceo', d)
    b = DepartManager('ls', 'dm', c)
    a = Supervisor('zs', 'sp', b)
    a.handle(req)
