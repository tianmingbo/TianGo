# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 11:19
# @Author  : tmb
from socket import *

udpServer = socket(AF_INET, SOCK_DGRAM)
udpServer.bind(('0.0.0.0', 22222))
while True:
    data, addr = udpServer.recvfrom(1024)
    print(data.decode('utf-8'))
    udpServer.sendto(data, addr)
    print('received and returned', addr)
udpServer.close()
