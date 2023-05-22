from abc import ABCMeta, abstractmethod


class Subject(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @abstractmethod
    def request(self, content):
        pass


class RealSubject(Subject):
    """
    真实类
    """

    def request(self, content):
        print(f'RealSubject to do something')


class ProxySubject(Subject):
    """代理类"""

    def __init__(self, name, subject):
        super(ProxySubject, self).__init__(name)
        self._real_subject = subject

    def request(self, content=''):
        self.pre_request()
        if self._real_subject:
            # 调用目标类实现真正的请求
            self._real_subject.request(content)
        self.after_request()

    @staticmethod
    def pre_request():
        print('set ip')

    @staticmethod
    def after_request():
        print('deal data')


if __name__ == '__main__':
    real_obj = RealSubject('real')
    proxy_obj = ProxySubject('proxy', real_obj)
    proxy_obj.request()
