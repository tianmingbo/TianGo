def average():
    count = 0
    num = 0
    res = None
    while True:
        cur_num = yield
        if cur_num is None:
            break  # 退出条件
        count += cur_num
        num += 1
        res = count / num
    return res


if __name__ == "__main__":
    gen = average()  # 创建生成器对象
    """
    在调用send发送非none值之前，*必须* 激活协程（预激），方式有两种1. gen.send(None), 2. next(gen)
    让协程向前执行到第一个yield表达式，准备好作为活跃的协程使用
    """
    url = gen.send(None)
    gen.send(1)  # send方法可以传递值进入生成器内部，同时还可以重启生成器执行到下一个yield位置
    gen.send(3)
    try:
        gen.send(None)  # 发送None会终止协程，返回结果，生成器抛出StopIteration异常，异常对象的value保存返回的值(>>奇葩)
    except StopIteration as e:
        print(e.value)
