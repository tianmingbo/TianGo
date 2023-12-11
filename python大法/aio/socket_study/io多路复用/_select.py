"""
如果用 C 实现多路复用，那么会以文件描述符作为参数，有了文件描述符，函数就能找到对应的套接字，进而进行监听、读写等操作。
但在 Python 里面，则是直接使用套接字本身作为参数，而不是使用文件描述符

缺点：
    每一次监听都要将所有的文件描述符拷贝到内核态，如果描述符非常多的话，这种拷贝会很耗时；
    当事件发生时，还要将所有的文件描述符都遍历一次，才能找到那些有事件发生的套接字。如果描述符非常多，遍历也需要时间；
    最多同时监听 1024 个文件描述符。
"""
import socket
import select
from queue import Queue
from typing import Dict

server = socket.socket()
server.bind(("localhost", 12345))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
# 必须设置为非阻塞，IO 多路复用要搭配非阻塞套接字
server.setblocking(False)
server.listen(5)

# 以上我们就创建了监听套接字，它负责监听是否有客户端连接
# 所以当事件发生时，属于可读事件，代表客户端连接过来了
# 所以 server 应该放在 rlist 里面
rlist = [server]
wlist = []
xlist = rlist
# 因为可以监听多个套接字，所以 rlist、wlist、xlist 都是列表
# 但在初始状态下，select 只需要监听一个套接字（server）即可

message_queues: Dict[socket.socket, Queue] = {}

while True:
    """
    select 函数接收四个参数
        rlist：一个列表，监听那些可读的 socket
        wlist：一个列表，监听那些可写的 socket
        xlist：一个列表，监听那些出错的 socket
        timeout：超时时间
    """
    # 开启 select 监听，返回三个元素
    # readable：   rlist 中发生可读事件的 socket
    # writeable：  wlist 中发生可写事件的 socket
    # exceptional：xlist 中发生异常的 socket
    readable, writeable, exceptional = select.select(rlist, wlist, xlist)

    # 遍历 readable
    for r in readable:
        # 如果 r is server，则代表监听套接字有事件发生
        # 显然是客户端连接来了
        if r is server:
            # 监听套接字是非阻塞的，那么已连接套接字默认也是非阻塞的
            # 当然你也可以调用 conn.setblocking(False) 显式地设置一下
            conn, addr = server.accept()
            print(f"和客户端 {addr[0]}:{addr[1]} 建立连接")
            # 将已连接套接字添加到 rlist 中，让它也被 select 监听
            # 当客户端发消息时，它会进入活跃状态，有事件发生
            # 然后被 select 监测到，放到 readable 中，这样遍历的时候就可以处理它了
            rlist.append(conn)
            # 由于客户端连接之后要发消息，那么我们是不是要将消息保存起来呢？
            message_queues[conn] = Queue()  # 负责保存后续客户端发的消息
        else:
            # 如果 r is not server，则代表是已连接套接字有事件发生
            # 说明是某个客户端发送消息了，我们要处理它
            data = r.recv(1024)
            if data:
                # 这里的 r 就是活跃的已连接套接字，调用它的 getpeername 方法
                # 也可以获取到客户端连接的 ip 和 端口
                addr = r.getpeername()
                print(f"收到客户端 {addr[0]}:{addr[1]} 发来的消息:",
                      f"`{data.decode('utf-8')}`")
                # message_queues 保存了所有的已连接套接字
                # 每一个套接字都对应一个队列，找到该活跃套接字对应的队列
                message_queues[r].put(data)  # 将消息放进去

                # 消息放进去了，服务端是不是也要回复呢？显然这属于可写事件
                # 我们还要将 r 放到 wlist 中，这样 select 就会监测到
                # 然后将它放到 writeable 中，我们遍历的时候就可以处理它了
                if r not in wlist:
                    wlist.append(r)
            else:
                # 走到这里说明 data 为假，说明客户端断开连接了，发来一个 b''
                addr = r.getpeername()
                print(f"客户端 {addr[0]}:{addr[1]} 已断开连接")
                # 我们要将套接字从 rlist、wlist 当中移除
                # 客户端都断开连接了，那么 select 也就不需要再监听了
                rlist.remove(r)
                if r in wlist:
                    wlist.remove(r)
                # 对了，还要将它从 message_queues 里面移除
                message_queues.pop(r)
                r.close()  # 关闭套接字连接

    # 以上是遍历可读事件，可读事件可以发生在监听套接字上面（和客户端建立连接）
    # 也可以发生在已连接套接字上面（客户端发信息了）
    # 如果没有事件发生或者处理完毕，那么接下来就要遍历可写事件
    # 而可写事件一定发生在已连接套接字上面（要回消息给客户端）
    for w in writeable:
        message_queue = message_queues[w]
        # 一开始队列里面肯定是有消息的，因为我们手动往里面放了一条
        # 但如果队列为空，说明服务端已经回复过了，那么要将该套接字从 wlist 里面移除
        # 让它变为非活跃状态，不再满足可写
        # 等到下一次客户端发消息时，再将它添加到 wlist 中，让它变得可写
        if message_queue.empty():
            wlist.remove(w)
            continue
        # 获取消息
        data = message_queue.get()
        # 发送给客户端
        w.send("服务端收到，你发的消息是: ".encode("utf-8") + data)

    # 然后遍历 xlist，如果在跟某个客户端通信的过程中，出现了错误
    # 那么将套接字从 rlist、wlist、xlist、message_queue 当中都删除
    # 然后再关闭套接字连接
    for x in exceptional:
        addr = x.getpeername()
        print(f"和客户端 {addr[0]}:{addr[1]} 通信出现错误")
        rlist.remove(x)
        if x in wlist:
            wlist.remove(x)
        message_queues.pop(x)
        x.close()
