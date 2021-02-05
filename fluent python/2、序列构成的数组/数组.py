# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 22:21
# @Author  : tmb
from array import array
from random import random

floats = array('d', (random() for i in range(10 ** 7)))
print(floats[-1])
# fp=open('floats.bin','wb')
# floats.tofile(fp) #写入文件
# fp.close()
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10 ** 7)  # 读取文件
fp.close()
print(floats2[-2])
