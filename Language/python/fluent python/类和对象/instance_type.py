class A:
    pass


class B(A):
    pass


if __name__ == '__main__':
    b = B()
    print(isinstance(b, B))  # True
    print(isinstance(b, A))  # True 会查看继承关系
    print(type(b) is A)  # False
