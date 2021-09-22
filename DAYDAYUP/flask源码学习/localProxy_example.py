class Boss(object):
    def task1(self):
        print('this is task1')

    def task2(self):
        print('this is task2')


class Proxy(object):
    def __init__(self, obj):
        self.proxy = obj

    def task1(self):
        self.proxy.task1()

    def task2(self):
        self.proxy.task2()


proxy_boss = Proxy(Boss())


class Client(object):
    def do_something(self):
        proxy_boss.task1()


if __name__ == '__main__':
    c = Client()
    c.do_something()
