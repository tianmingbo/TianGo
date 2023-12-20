import asyncio
from asyncio import Lock


class MockSocket:

    def __init__(self):
        self.socket_closed = False

    async def send(self, msg: str):
        # 模拟向客户端缓慢发送消息
        if self.socket_closed:
            raise Exception("socket 已关闭")
        print(f"准备向客户端发送消息: {msg}")
        await asyncio.sleep(1)
        print(f"成功向客户端发送消息: {msg}")

    def close(self):
        self.socket_closed = True


usernames_to_sockets = {"satori": MockSocket(), "koishi": MockSocket(),
                        "marisa": MockSocket(), "scarlet": MockSocket()}


async def user_disconnect(username: str, lock: Lock):
    # 断开用户连接，并将其从应用程序内存中删掉
    print(f"{username} 断开连接")
    async with lock:
        socket = usernames_to_sockets.pop(username)
        socket.close()


async def message_all_users(lock: Lock):
    # 同时向所有用户发送消息
    print(f"创建消息发送任务")
    async with lock:
        messages = [socket.send(f"Hello {username}") for username, socket in usernames_to_sockets.items()]
        await asyncio.gather(*messages)


async def main():
    lock = Lock()
    await asyncio.gather(message_all_users(lock), user_disconnect("marisa", lock))


asyncio.run(main())
"""
创建消息发送任务
marisa 断开连接
准备向客户端发送消息: Hello satori
准备向客户端发送消息: Hello koishi
准备向客户端发送消息: Hello scarlet
Traceback (most recent call last):
  ......
    raise Exception("socket 已关闭")
Exception: socket 已关闭
"""
