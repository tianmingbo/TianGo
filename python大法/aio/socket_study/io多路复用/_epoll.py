import select
import socket
from queue import Queue
from select import (
    # epoll 和 poll 的用法相似
    # 把事件换成 epoll 的事件即可
    EPOLLIN,
    EPOLLOUT,
    EPOLLERR,
    EPOLLHUP
)
from typing import Dict

server = socket.socket()
server.bind(("localhost", 12345))
server.setsockopt(socket.SOL_SOCKET,
                  socket.SO_REUSEADDR, True)
server.setblocking(False)
server.listen(5)

fd2sk = {server.fileno(): server}
message_queues: Dict[int, Queue] = {}

# 实例化一个 epoll 对象
epoll = select.epoll()
# 给 server 注册读事件
epoll.register(server, EPOLLIN | EPOLLERR)

while True:
    # 仍然是调用 poll 方法，开始轮询
    events = epoll.poll()
    for fd, event in events:
        if fd == server.fileno():
            conn, addr = fd2sk[fd].accept()
            print(f"和客户端 {addr[0]}:{addr[1]} 建立连接")
            # 给已连接套接字注册读事件
            # 第一个参数可以传文件描述符、也可以传套接字
            epoll.register(conn, EPOLLIN | EPOLLHUP | EPOLLERR)
            fd2sk[conn.fileno()] = conn
            message_queues[conn.fileno()] = Queue()

        elif event & EPOLLIN:  # 可读
            data = fd2sk[fd].recv(1024)
            if data:  # 有数据
                addr = fd2sk[fd].getpeername()
                print(f"收到客户端 {addr[0]}:{addr[1]} 发来的消息:",
                      f"`{data.decode('utf-8')}`")
                # 客户端发消息了，那么套接字要回复消息，因此满足可写
                # 但是和 poll 不同，epoll 只能给一个套接字注册一次
                # 而之前已经注册过一次了（已连接套接字创建时，注册了读事件）
                # 因此再注册就会报错，因为不能连续注册
                # 所以我们需要将 fd 上的事件取消掉，然后重新注册
                epoll.unregister(fd)
                # 重新注册，此时要同时注册读事件和写事件
                epoll.register(fd, EPOLLIN | EPOLLOUT | EPOLLHUP | EPOLLERR)
                message_queues[fd].put(data)
            else:
                # 客户端断开连接了
                addr = fd2sk[fd].getpeername()
                print(f"客户端 {addr[0]}:{addr[1]} 已断开连接")
                epoll.unregister(fd)
                fd2sk[fd].close()
                fd2sk.pop(fd)

        elif event & EPOLLOUT:  # 可写
            message_queue = message_queues[fd]
            if message_queue.empty():
                # 队列是空的，说明消息已经发走了，那么应该取消写事件
                # 做法也很简单：先将事件全部取消，然后重新注册读事件
                # 但也可以通过 modify 方法，直接修改事件类型
                epoll.modify(fd, EPOLLIN | EPOLLHUP | EPOLLERR)
            else:
                data = message_queue.get()
                fd2sk[fd].send(
                    "服务端收到，你发的消息是: ".encode("utf-8") + data
                )
        elif event & EPOLLERR:
            addr = fd2sk[fd].getpeername()
            print(f"和客户端 {addr[0]}:{addr[1]} 通信出现错误")
            epoll.unregister(fd)
            fd2sk[fd].close()
            message_queues.pop(fd)
