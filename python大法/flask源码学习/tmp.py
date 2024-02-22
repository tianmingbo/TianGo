def test(q):
    print(q)
    return 'dfa'


class Descriptor:
    def __get__(self, instance, owner):
        # 对属性的获取行为进行定制
        print("Getting attribute")
        return test


class MyClass:
    __getattr__ = Descriptor()


obj = MyClass()
value = obj.attr  # 触发 Descriptor 的 __get__ 方法
print(value)
