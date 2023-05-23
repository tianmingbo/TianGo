from abc import ABCMeta, abstractmethod


class ShippingStrategy(metaclass=ABCMeta):
    @abstractmethod
    def calculate(self, order):
        pass


class StandardShippingStrategy(ShippingStrategy):
    def calculate(self, order):
        return 10 + order.total_weight() * 2


class ExpressShippingStrategy(ShippingStrategy):
    def calculate(self, order):
        return 20 + order.total_weight() * 5


class SelfPickupStrategy(ShippingStrategy):
    def calculate(self, order):
        return 0


class Order:
    def __init__(self, items, seller, destination):
        self.items = items
        self.seller = seller
        self.destination = destination

    def total_weight(self):
        return sum(item['weight'] for item in self.items)


# context
class ShippingCalculator:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def calculate_shipping_fee(self, order):
        return self.strategy.calculate(order)


if __name__ == '__main__':
    ship1 = ShippingCalculator(StandardShippingStrategy())
    ship2 = ShippingCalculator(ExpressShippingStrategy())
    ship3 = ShippingCalculator(SelfPickupStrategy())
    order = Order([{'weight': 1}, {'weight': 2}], 'dali', '')
    print(
        ship1.calculate_shipping_fee(order),
        ship2.calculate_shipping_fee(order),
        ship3.calculate_shipping_fee(order),
    )
