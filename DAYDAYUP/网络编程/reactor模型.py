"""
reactor模型是一种高效的事件驱动设计模式,非常适合构建高性能、高并发的网络程序。

reactor模型主要有以下几个组件:
    Reactor(反应器):负责监听事件(网络IO事件、用户输入等),当事件发生时分发调用处理程序。是整个事件循环的核心。
    Handlers(处理程序):执行对事件的响应,实现业务逻辑。事件发生时由Reactor调用。
    Event Demultiplexer(事件分离器):底层的事件通知机制,不同平台有不同实现(如epoll、select等)。将事件通知给Reactor。
    Event Loops(事件循环):不断循环执行事件处理任务的机制。一般由Reactor控制。
    
它的工作流程如下:
    应用注册处理程序,处理不同事件
    Reactor通过调用事件分离器等待事件 ready
    事件发生,分离器通知Reactor
    Reactor dispatch事件调用对应的Handler来响应
    Handler完成处理后,继续等待新的事件
reactor模型充分利用了事件驱动设计,可以高效地处理大量并发请求。采用单线程也避免了锁的开销。
"""
import selectors
import socket


class Reactor:

    def __init__(self):
        self.selector = selectors.DefaultSelector()
        self.fd_callbacks = {}

    def register(self, fd, callback):
        self.selector.register(fd, selectors.EVENT_READ, callback)
        self.fd_callbacks[fd] = callback

    def run(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = self.fd_callbacks[key.fd]
                callback(key.fd)


reactor = Reactor()


def read_callback(fd):
    print(f'Data is ready to read on fd {fd}')


def write_callback(fd):
    print(f'Ready to write on fd {fd}')


sock1 = socket.socket()
sock1.bind(('localhost', 8000))

sock2 = socket.socket()
sock2.bind(('localhost', 8001))

reactor.register(sock1, read_callback)
reactor.register(sock2, write_callback)

reactor.run()
