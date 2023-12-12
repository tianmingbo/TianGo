import asyncio
import socket
from asyncio import AbstractEventLoop


async def echo(conn: socket.socket, loop: AbstractEventLoop):
    # 无限循环等待来自客户端连接的数据
    while data := await loop.sock_recv(conn, 1024):
        # 收到数据之后再将其发送给客户端
        # 为了区别，我们发送的时候在结尾加一个 b"~"
        await loop.sock_sendall(conn, data + b"~")


async def listen_for_conn(server: socket.socket):
    while True:
        loop = asyncio.get_event_loop()
        conn, addr = await loop.sock_accept(server)
        conn.setblocking(False)
        print(f"收到客户端 {addr} 的连接")
        # 每当获得连接时，创建一个任务来监听客户端的数据
        asyncio.create_task(echo(conn, loop))


async def main():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server.setblocking(False)
    server.bind(("localhost", 12345))
    server.listen()

    # 其实这个 loop 参数是没有必要传的，直接在协程里面通过 get_running_loop 获取即可
    await listen_for_conn(server)


asyncio.run(main())
