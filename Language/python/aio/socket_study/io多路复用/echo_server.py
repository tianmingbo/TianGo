import asyncio
import socket
from asyncio import AbstractEventLoop
from typing import List
import signal


async def echo(conn: socket.socket, loop: AbstractEventLoop):
    try:
        while data := await loop.sock_recv(conn, 1024):
            await loop.sock_sendall(conn, data + b"~")
    except Exception as e:
        print(e)
    finally:
        conn.close()


echo_tasks = []


async def listen_for_conn(server: socket.socket):
    loop = asyncio.get_event_loop()
    while True:
        conn, addr = await loop.sock_accept(server)
        conn.setblocking(False)
        print(f"收到客户端 {addr} 的连接")
        # 每当获得连接时，创建一个任务来监听客户端的数据
        echo_task = asyncio.create_task(echo(conn, loop))
        echo_tasks.append(echo_task)


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    # 每个任务等待两秒钟
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    # 这里采用循环，关于同时等待多个任务，后续有更好的做法
    for task in waiters:
        try:
            await task
        except asyncio.TimeoutError:
            pass


async def main():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server.setblocking(False)
    server.bind(("localhost", 12345))
    server.listen()

    loop = asyncio.get_running_loop()
    # 捕捉信号，退出程序，exit(0) 本质上就是 raise 一个 SystemExit 异常
    for sig_name in ("SIGINT", "SIGTERM"):
        loop.add_signal_handler(getattr(signal, sig_name), lambda: exit(0))

    await listen_for_conn(server)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except SystemExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
