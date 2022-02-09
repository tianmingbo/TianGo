# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 10:03
# @Author  : tmb
from socket import *

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(('0.0.0.0', 22222))
tcpServer.listen()
while True:
    print('waiting for connection……')
    tcpClient, addr = tcpServer.accept()
    print('...connected from', addr)
    while True:
        data = tcpClient.recv(1024)
        print(data, type(data))
        if data.decode('utf-8') == 'end':
            break
        tcpClient.send(data)
    tcpClient.close()
tcpServer.close()

'''
ss = socket() # 创建服务器套接字
ss.bind() # 套接字与地址绑定
ss.listen() # 监听连接
inf_loop: # 服务器无限循环
    cs = ss.accept() # 接受客户端连接
    comm_loop: # 通信循环
        cs.recv()/cs.send() # 对话（接收/发送）
    cs.close() # 关闭客户端套接字
ss.close() # 关闭服务器套接字#（可选）
'''
