# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 11:19
# @Author  : tmb
from socket import *

udpClient = socket(AF_INET, SOCK_DGRAM)
ADDR = ('127.0.0.1', 22222)
while True:
    data = input('< ')
    if not data:
        break
    udpClient.sendto(data.encode('utf-8'), ADDR)
    data, addr = udpClient.recvfrom(1024)
    if not data:
        break
    print(data.decode('utf-8'))
udpClient.close()
