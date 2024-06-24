from concurrent.futures import Future

future = Future()


def callback(future):
    print("当set_result的时候，执行回调，我也可以拿到返回值：", future.result())


# 通过调用add_done_callback方法，可以将该future绑定一个回调函数
# 这里只需要传入函数名即可，future会自动传递给callback的第一个参数
# 如果这里需要多个参数的话，怎么办呢？很简单，使用偏函数即可
future.add_done_callback(callback)

# 当什么时候会触发回调函数的执行呢？
# 当future执行set_result的时候
future.set_result("return value")
"""
当set_result的时候，执行回调，我也可以拿到返回值： return value
"""
