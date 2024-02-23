from functools import partial


class C:
    attr = 'test'


class Descriptor:

    def __get__(self, instance, owner):
        a = C()
        print("Getting attribute")
        return partial(getattr, a)


class MyClass:
    __getattr__ = Descriptor()
    # def __getattr__(self, item):
    #     print(item)
    #     print("Getting attribute")
    #     return getattr(C(), item)


obj = MyClass()
value = obj.attr
print(value)
