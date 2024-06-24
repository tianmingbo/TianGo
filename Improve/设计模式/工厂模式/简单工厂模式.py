from abc import ABCMeta, abstractmethod


class Coffee(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @abstractmethod
    def get_taste(self):
        pass


class LatteCoffee(Coffee):
    def __init__(self, name):
        super().__init__(name)

    def get_taste(self):
        return 'nan he'


class MochaCoffee(Coffee):
    def __init__(self, name):
        super(MochaCoffee, self).__init__(name)

    def get_taste(self):
        return 'so nan he'


class CoffeeMaker:
    """
    专门定义一个类用来创建其他类，根据参数不同创建不同的类的实例，
    被创建的实例通常有共同的父类，这就是简单工厂模式
    """
    @staticmethod
    def make_coffee(coffee_bean):
        if coffee_bean == 'natie':
            coffee = LatteCoffee(coffee_bean)
        elif coffee_bean == 'moka':
            coffee = MochaCoffee(coffee_bean)
        else:
            raise ValueError(f'{coffee_bean} 类型不支持')
        return coffee


if __name__ == '__main__':
    latte = CoffeeMaker.make_coffee('natie')
    print(f'{latte.get_name()},味道{latte.get_taste()}')
    latte = CoffeeMaker.make_coffee('moka')
    print(f'{latte.get_name()},味道{latte.get_taste()}')
