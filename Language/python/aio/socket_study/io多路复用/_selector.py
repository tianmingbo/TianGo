import socket
from queue import Queue

# selectors 里面提供了多种"多路复用器"
# 除了 select、poll、epoll 之外
# 还有 kqueue，这个是针对 BSD 平台的
try:
    from selectors import (
        SelectSelector,
        PollSelector,
        EpollSelector,
        KqueueSelector
    )
except ImportError:
    pass
# 由于种类比较多，所以提供了 DefaultSelector
# 会根据当前的系统种类，自动选择一个合适的多路复用器
from selectors import (
    DefaultSelector,
    EVENT_READ,  # 读事件
    EVENT_WRITE,  # 写事件
)

server = socket.socket()
server.bind(("localhost", 12345))
server.setsockopt(socket.SOL_SOCKET,
                  socket.SO_REUSEADDR, True)
server.setblocking(False)
server.listen(5)

message_queues = {}
# 实例化一个多路复用器
sel = DefaultSelector()


def accept(server: socket.socket):
    """和客户端建立连接"""
    conn, addr = server.accept()
    print(f"和客户端 {addr[0]}:{addr[1]} 建立连接")
    # 一旦建立连接，那么就要接收客户端消息
    # 所以我们要绑定事件，register 方法接收三个参数
    # 参数一：传一个套接字即可
    # 参数二：事件类型，这里是读事件
    # 参数三：事件发生时，执行的回调函数
    sel.register(conn, EVENT_READ, recv)
    # 表示当 conn 可读时，就去执行 recv 函数
    message_queues[conn] = Queue()


def recv(conn: socket.socket):
    """接收客户端数据"""
    data = conn.recv(1024)
    addr = conn.getpeername()
    if data:  # 有数据
        print(f"收到客户端 {addr[0]}:{addr[1]} 发来的消息:",
              f"`{data.decode('utf-8')}`")
        # 收到数据了，那么要给客户端回复，所以要绑定可写事件
        # 让事件可写，当事件发生时，执行 send 函数
        sel.modify(conn, EVENT_READ | EVENT_WRITE, send)
        message_queues[conn].put(data)
    else:
        print(f"客户端 {addr[0]}:{addr[1]} 已断开连接")
        conn.close()
        # 取消监听
        sel.unregister(conn)
        message_queues.pop(conn)


def send(conn: socket.socket):
    """给客户端发送数据"""
    message_queue = message_queues[conn]
    if message_queue.empty():
        # 队列为空说明已经发送过了，将事件改成可读
        # 继续监听客户端发来的消息
        sel.modify(conn, EVENT_READ, recv)
    else:
        data = message_queue.get()
        conn.send(
            "服务端收到，你发的消息是: ".encode("utf-8") + data
        )


# 给监听套接字注册可读事件
# 当有客户端连接，去执行 accept 函数
sel.register(server, EVENT_READ, accept)
# 在 accept 函数里面创建已连接套接字 conn
# 然后给 conn 绑定可读事件，当客户端发消息时，去执行 recv 函数
# 在 recv 函数里面给套接字绑定可写事件，然后去执行 send 函数

while True:
    # 内部会根据操作系统，选择一个合适的多路复用
    events = sel.select()
    # key 是一个 namedtuple
    # 内部有如下字段：'fileobj', 'fd', 'events', 'data'
    # key.fd 就是套接字的文件描述符
    # key.fileobj 则是套接字本身
    # key.data 是给套接字绑定的回调
    # key.event 则是事件
    for key, mask in events:
        # 事件发生时，获取回调，然后调用
        # 回调显然就是这里的 accept、recv、send
        callback = key.data
        callback(key.fileobj)
