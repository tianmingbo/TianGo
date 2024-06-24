class ClassDecorator:
    def __init__(self, func):
        self.__num_of_call = 0
        self.__func = func

    def __call__(self, *args, **kwargs):
        self.__num_of_call += 1
        obj = self.__func(*args, **kwargs)
        print(f'创建{self.__func.__name__}的第{self.__num_of_call}的实例')
        return obj


@ClassDecorator
class MyClass:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


if __name__ == '__main__':
    a = MyClass('tian')
    print(a.get_name)
    b = MyClass('tian2')
    print(b.get_name)
