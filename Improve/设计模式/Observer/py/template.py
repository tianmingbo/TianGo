from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """
    观察者基类
    """

    def update(self, observable, obj):
        pass


class Observable:
    """被观察者基类"""

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        """添加观察者"""
        self.__observers.append(observer)

    def remove_observer(self, observer):
        """删除观察者"""
        self.__observers.remove(observer)

    def notify_observer(self, obj=0):
        """
        内容或状态发生变化时，通知所有观察者
        """
        for o in self.__observers:
            o.update(self, obj)
