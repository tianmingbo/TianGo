from abc import abstractmethod, ABCMeta


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def say(self):
        """必须被子类实现"""
        pass


class Dog(Animal):
    def say(self):
        print('hello')


if __name__ == '__main__':
    dog = Dog()
    dog.say()
