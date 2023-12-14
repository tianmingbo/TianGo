from threading import Thread
import socket


class EchoThread(Thread):

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        try:
            while True:
                data = self.conn.recv(1024)
                # 客户端断开连接时，返回 b""
                if not data:
                    # BrokenPipeError 继承自 OSError
                    raise BrokenPipeError("连接断开")
                print(f"收到数据: {data}")
                self.conn.sendall(data + b"~")
        except OSError:
            print(f"线程 shutdown")

    def close(self):
        # 如果线程处于活跃状态，则关闭连接
        if self.is_alive():
            self.conn.sendall(b"shutdown")
            # 不再和客户端进行数据的读取和写入，但是连接依旧保持着
            self.conn.shutdown(socket.SHUT_RDWR)
            # 所以再调用一个 close 方法
            self.conn.close()


with socket.socket() as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 9999))
    server.listen()
    connection_threads = []
    try:
        while True:
            conn, addr = server.accept()
            thread = EchoThread(conn)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print("主线程收到 Ctrl+C 引发的 KeyboardInterrupt")
        for t in connection_threads:
            # 在每个子线程上调用 close 方法，以便于在主线程收到中断时，关闭每个客户端连接
            t.close()
