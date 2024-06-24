from abc import ABCMeta, abstractmethod


# 策略接口
class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


# 具体策略类
class ConcreteStrategyA(Strategy):
    def execute(self):
        print("Executing Concrete Strategy A...")


class ConcreteStrategyB(Strategy):
    def execute(self):
        print("Executing Concrete Strategy B...")


# 定义策略上下文类：策略上下文类封装了策略对象的创建和调用过程，并提供了客户端调用策略的方法
class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute_strategy(self) -> None:
        self._strategy.execute()


if __name__ == '__main__':
    context = Context(ConcreteStrategyA())
    context.execute_strategy()

    context.set_strategy(ConcreteStrategyB())
    context.execute_strategy()
