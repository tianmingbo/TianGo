import socketserver


# 自定义一个类，必须继承 BaseRequestHandler
class ServiceHandler(socketserver.BaseRequestHandler):
    """
    内部提供了三个重要属性
        self.request: 已连接套接字 conn
        self.client_address: 客户端信息 addr
        self.server: 服务端实例（一会我们会创建它）

    然后我们必须要实现 handle 方法，处理客户端连接时会自动调用
    此外还有两个方法，分别是 setup 和 finish，实不实现均可
    """

    def setup(self) -> None:
        """在执行 handle 之前调用，用于提前做一些连接相关的设置"""

    def finish(self) -> None:
        """在执行 handle 之后调用，用于资源释放等等"""
        self.request.close()

    def handle(self) -> None:
        """
        处理客户端连接
        这里的 self.request 就相当于之前的 conn
        """
        client_ip, client_port = self.client_address
        while True:
            msg = self.request.recv(1024)
            if not msg:
                print(f"客户端(ip: {client_ip}, port: {client_port}) 已经断开连接")
                self.request.close()
                break
            print(f"客户端(ip: {client_ip}, port: {client_port}) 发来消息:",
                  msg.decode("utf-8"))
            self.request.send("服务端收到, 你发的消息是: ".encode("utf-8") + msg)


# 绑定 IP 和端口，以及用于处理的 Handler
# 这里的 ThreadingTCPServer 实例就是 ServiceHandler 里面的 self.server
server = socketserver.ThreadingTCPServer(
    ("localhost", 12346),
    ServiceHandler
)
# 开启无限循环，监听连接
server.serve_forever()
# 如果关闭监听，那么调用 server.shutdown()
