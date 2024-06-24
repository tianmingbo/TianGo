import weakref

s1 = {1, 2, 3}
s2 = s1


def bye():
    print('Done')


if __name__ == '__main__':
    # 垃圾回收
    ender = weakref.finalize(s1, bye)  # 在s1引用注册bye回调
    print(ender.alive)
    del s1
    print(ender.alive)  # del不删除对象，而是删除对象的引用
    s2 = 'test'  # 重新绑定s2，s1的引用为0，对象销毁，调用bye
    print(ender.alive)
