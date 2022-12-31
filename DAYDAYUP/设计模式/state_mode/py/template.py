from abc import ABCMeta, abstractmethod


def singleton(cls, *args, **kwargs):
    """
    每一种状态只有一个实例
    """
    instance = {}

    def __singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return __singleton


class State:
    """
    状态的基类
    """

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def is_match(self, state_info):
        return False

    @abstractmethod
    def show(self, context):
        pass


class Context(metaclass=ABCMeta):
    """
    状态模式中的上下文环境类
    """

    def __init__(self):
        self.__states = []
        self.__cur_state = None
        # 状态发生变化时依赖的属性,当由多个属性共同决定时,可以添加一个类
        self.__state_info = 0

    def add_state(self, state):
        # 添加状态
        if state not in self.__states:
            self.__states.append(state)

    def change_state(self, state):
        if state is None:
            return
        if self.__cur_state is None:
            print("初始化为:", state.get_name())
        else:
            print(f"由{self.__cur_state.get_name()}切换到{state.get_name()}")
        self.__cur_state = state
        self.add_state(state)
        return True

    def get_state(self):
        return self.__cur_state

    def _set_state_info(self, state_info):
        """
        如果满足某个状态，就切换到对应状态
        """
        self.__state_info = state_info
        for state in self.__states:
            if state.is_match(state_info):
                self.change_state(state)

    def _get_state_info(self):
        return self.__state_info
