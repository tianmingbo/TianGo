from socket import *
import time

udp_socket = None
feiQ_port = 2425
feiQ_version = 1
feiQ_user_name = "dongge-test"
feiQ_host_name = "mac-pro"
broadcast_ip = "255.255.255.255"

# 飞秋command
IPMSG_BR_ENTRY = 0x00000001  # 表示 上线提醒


def create_udp_socket():
    """创建udp套接字"""
    global udp_socket

    # 1. 创建socket
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    # 2. 绑定2425端口
    udp_socket.bind(("", feiQ_port))
    # 3. 设定允许广播
    # 默认情况下 一个程序是不能发送广播数据（就是当前局域网内所有的电脑都能收到数据），需要下面代码来进行设定
    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


def send_broadcast_online():
    """发送上线广播"""

    # demo如下
    # 1:1500816649:dongge-test:mac-pro:1:dongge-test
    # 拼装一个飞鸽传书的数据包
    msg = "%d:%d:%s:%s:%d:%s" % (feiQ_version, int(time.time()), feiQ_user_name, feiQ_host_name, IPMSG_BR_ENTRY, feiQ_user_name)

    # print(msg)  # for test

    # 因为windows是使用是gbk编码所以需要编码为gbk
    udp_socket.sendto(msg.encode('gbk'), (broadcast_ip, feiQ_port))


def main():
    """完成整体控制"""

    # 1. 创建udp套接字
    create_udp_socket()

    # 2. 发送上线广播
    send_broadcast_online()


if __name__ == '__main__':
    main()