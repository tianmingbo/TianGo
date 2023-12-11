import socket
import select
from select import POLLIN, POLLOUT, POLLERR, POLLHUP
from typing import Dict
from queue import Queue

server = socket.socket()
server.bind(("localhost", 12345))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server.setblocking(False)
server.listen(5)

# 通过文件描述符找到套接字
fd2sk = {server.fileno(): server}
# 保存套接字接收到的客户端发来的消息
message_queues: Dict[int, Queue] = {}

# 实例化一个 poll 对象
poll = select.poll()

# 给指定的套接字绑定事件
# 第一个参数可以是描述符，也可以是套接字
# 第二个参数是要绑定的事件
# POLLIN：可读事件（rlist）
# POLLOUT：可写事件（wlist）
# POLLERR：出现异常（xlist）
# POLLHUP：连接中断
# 首先要对 server 进行注册，正如我们使用 select.select 时
# 要先将 server 放在 rlist 里面，然后事件为可读
# 不过由于可能发生错误，因此事件类型为 POLLIN | POLLERR
poll.register(server, POLLIN | POLLERR)

# 开启无限循环
while True:
    # poll 方法接收一个 timeout，不传则表示不设置超时
    # 它和 select.select 的第四个参数的含义相同
    # 当有事件发生时，会返回相应的文件描述符和事件
    events = poll.poll()  # 正式开启监听
    # 我们进行遍历
    for fd, event in events:
        # 说明是监听套接字活跃了
        if fd == server.fileno():
            conn, addr = fd2sk[fd].accept()
            print(f"和客户端 {addr[0]}:{addr[1]} 建立连接")
            # 对 conn 进行注册，下一轮循环的时候也会对它进行监听
            # 这里可以传文件描述符、也可以传套接字
            # 如果传套接字，那么会自动调用 fileno 获取描述符
            poll.register(conn, POLLIN | POLLHUP | POLLERR)
            # 维护文件描述符到套接字的映射
            fd2sk[conn.fileno()] = conn
            # 为每个文件描述符维护一个队列，用于保存客户端发来的消息
            message_queues[conn.fileno()] = Queue()

        # 否则说明是已连接套接字有事件发生
        # 那么事件是可读还是可写呢？显然要通过 event 判断
        elif event & POLLIN:  # 可读
            data = fd2sk[fd].recv(1024)
            if data:  # 有数据
                addr = fd2sk[fd].getpeername()
                print(f"收到客户端 {addr[0]}:{addr[1]} 发来的消息:",
                      f"`{data.decode('utf-8')}`")
                # 客户端发消息，服务端也要回消息
                # 因此要给它注册一个可写事件
                poll.register(fd, POLLOUT | POLLHUP | POLLERR)
                # 然后将消息保存起来
                message_queues[fd].put(data)
            else:  # 客户端断开连接
                addr = fd2sk[fd].getpeername()
                print(f"客户端 {addr[0]}:{addr[1]} 已断开连接")
                # 取消监听，会将所有事件全部取消
                poll.unregister(fd)
                # 关闭连接
                fd2sk[fd].close()
                # 从字典中移除
                fd2sk.pop(fd)
        elif event & POLLOUT:  # 已连接套接字可写
            message_queue = message_queues[fd]
            if message_queue.empty():
                # 队列为空，说明消息已经发出去了
                # 那么套接字就不再可写了，因此要取消监听
                # 等到下一次客户端发消息时，再变得可写
                poll.unregister(fd)
                # 但 unregister 会取消所有事件的监听
                # 因此还要重新注册可读事件
                # 不然后续客户端发消息时，就无法处理了
                poll.register(fd, POLLIN | POLLHUP | POLLERR)
            else:
                data = message_queue.get()
                fd2sk[fd].send(
                    "服务端收到，你发的消息是: ".encode("utf-8") + data
                )
        elif event & POLLERR:  # 发生错误
            addr = fd2sk[fd].getpeername()
            print(f"和客户端 {addr[0]}:{addr[1]} 通信出现错误")
            poll.unregister(fd)
            fd2sk[fd].close()
            message_queues.pop(fd)
