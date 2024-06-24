# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 14:03
# @Author  : tmb

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')
while True:
    # 断开消息就丢失了，连接上继续接收消息
    res = socket.recv()
    res = str(res, encoding='utf-8')
    print('res %s' % res)
