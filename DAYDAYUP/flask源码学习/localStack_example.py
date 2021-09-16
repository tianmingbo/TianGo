from local_example import LocalStack, LocalProxy
import random, threading, time

'''
LocalStack:
初始化的时候，会创建一个Local实例。LocalStack实现了push，pop，top方法。
调用这些方法时，会根据当前线程或协程的标识数值，在local实例中对相应的数值进行操作。
'''

# 生成一个LocalStack实例_stack
_stack = LocalStack()


# 定义一个RequestConetxt类，它包含一个上下文环境。
# 当调用这个类的实例时，它会将这个上下文对象放入
# _stack栈中去。当退出该上下文环境时，栈会pop其中
# 的上下文对象。

class RequestConetext(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __enter__(self):
        _stack.push(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            _stack.pop()

    def __repr__(self):
        return '%s, %s, %s' % (self.a, self.b, self.c)


# 定义一个可供不同线程调用的方法。当不同线程调用该
# 方法时，首先会生成一个RequestConetxt实例，并在这
# 个上下文环境中先将该线程休眠一定时间，之后打印出
# 目前_stack中的信息，以及当前线程中的变量信息。
# 以上过程会循环两次。

def worker(i):
    with request_context(i):
        pause = random.random()
        print('Sleeping %0.02f' % pause)
        time.sleep(pause)
        print('stack: %s' % _stack._local.__storage__.items())
        print('ident_func(): %d' % _stack.__ident_func__())
        print('a=%s; b=%s; c=%s' %
              (LocalProxy(lambda: _stack.top.a),
               LocalProxy(lambda: _stack.top.b),
               LocalProxy(lambda: _stack.top.c)))
    print('Done')


# 调用该函数生成一个RequestConetxt对象

def request_context(i):
    i = str(i + 1)
    return RequestConetext('a' + i, 'b' + i, 'c' + i)


# 在程序最开始显示_stack的最初状态
print('start', _stack._local.__storage__)

# 产生两个线程，分别调用worker函数
for i in range(2):
    t = threading.Thread(target=worker, args=(i,))
    t.start()

main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()

# 在程序最后显示_stack的最终状态
print('end', _stack._local.__storage__)
# if __name__ == '__main__':
#     l = LocalStack()
#     l.push(1)
#     print(l.top)
#     l.pop()
#     print(l.top)
