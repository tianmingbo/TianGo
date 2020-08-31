# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 11:37
# @Author  : tmb

import zmq
import time

# # 模式一
# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind('tcp://*:5555')
#
# while True:
#     message = socket.recv()
#     print('Received %s' % message)
#     socket.send_unicode('I am OK!')


# 模式二
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')

for i in range(10000000000):
    if i % 7 == 0 or ('7' in str(i)):
        socket.send(bytes(str(i),encoding='utf8'))
        time.sleep(1)
