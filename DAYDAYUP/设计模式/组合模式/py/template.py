from abc import ABCMeta, abstractmethod


class Component(metaclass=ABCMeta):
    """组件的基类"""

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @staticmethod
    def is_composite():
        # 判断是不是复合组件
        return False

    @abstractmethod
    def operation(self):
        pass


class Composite(Component):
    """复合组件，复合组件本身也是一个组件，可以像一般对象一样使用"""

    def __init__(self, name):
        super(Composite, self).__init__(name)
        self._components = []

    def add_component(self, component):
        self._components.append(component)

    def remove_component(self, component):
        self._components.remove(component)

    @staticmethod
    def is_composite():
        return True

    def operation(self):
        for component in self._components:
            component.operation()
