# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 10:03
# @Author  : tmb
from socket import *

tcpClient = socket(AF_INET, SOCK_STREAM)
tcpClient.connect(('127.0.0.1', 22222))
while True:
    data = input('>')
    tcpClient.send(data.encode('utf-8'))
    data = tcpClient.recv(1024)
    if not data:
        break
    print(data.decode('utf-8'))
tcpClient.close()
# '''
# cs = socket() # 创建客户端套接字
# cs.connect() # 尝试连接服务器
# comm_loop: # 通信循环
#     cs.send()/cs.recv() # 对话（发送/接收）
# cs.close() # 关闭客户端套接字
# '''
