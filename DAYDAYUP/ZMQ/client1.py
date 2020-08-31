# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 11:52
# @Author  : tmb
import zmq

# # 模式一
# context = zmq.Context()
# socket = context.socket(zmq.REQ)
# socket.connect('tcp://localhost:5555')
#
# socket.send_string("ok?")  # 发送
# res = socket.recv()  # 接收
# print('res %s' % res)


# 模式二
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')
while True:
    res = socket.recv()
    res=str(res,encoding='utf-8')
    print('res %s' % res)
