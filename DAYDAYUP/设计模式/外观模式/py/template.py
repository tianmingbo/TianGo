class SubsystemA:
    def operation_a1(self):
        print('Subsystem A: Operation A1')

    def operation_a2(self):
        print('Subsystem A: Operation A2')


class SubsystemB:
    def operation_b1(self):
        print('Subsystem B: Operation B1')

    def operation_b2(self):
        print('Subsystem B: Operation B2')


class Facade:
    def __init__(self):
        self._subsystem_a = SubsystemA()
        self._subsystem_b = SubsystemB()

    def operation_1(self):
        print('Facade: Operation 1')
        self._subsystem_a.operation_a1()
        self._subsystem_b.operation_b1()

    def operation_2(self):
        print('Facade: Operation 2')
        self._subsystem_a.operation_a2()
        self._subsystem_b.operation_b2()


def main():
    facade = Facade()

    facade.operation_1()
    facade.operation_2()


if __name__ == '__main__':
    main()
