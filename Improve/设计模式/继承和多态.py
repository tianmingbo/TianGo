from abc import ABCMeta, abstractmethod

"""
Pet类不能实例化对象，只能被其他类继承
abstractmethod装饰的方法，必须在子类中被重载
"""


class Pet(object, metaclass=ABCMeta):

    def __init__(self, nickname):
        self._nickname = nickname

    @abstractmethod
    def make_voice(self):
        '''发出声音'''
        print('123')


class Dog(Pet):
    '''狗'''

    def test(self):
        pass

    def make_voice(self):
        # 必须重载这个方法
        print('{}:汪汪汪～～～'.format(self._nickname))


def main():
    pet = Dog('lala')
    pet.make_voice()
    # pet = Pet('lala') #TypeError: Can't instantiate abstract class Pet with abstract methods make_voice
    # pet.make_voice() #TypeError:无法用抽象方法实例化抽象类Pet


if __name__ == "__main__":
    main()
