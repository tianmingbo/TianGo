class InteractiveObject:
    """进行交互的对象"""
    pass


class InteractiveObjectImplA:
    """实现类"""
    pass


class InteractiveObjectImplB:
    """实现类B"""
    pass


class Meditor:
    """中介类"""

    def __init__(self):
        self.__interactive_obj_a = InteractiveObjectImplA()
        self.__interactive_obj_b = InteractiveObjectImplB()

    def interative(self):
        """进行交互的操作"""
        pass
