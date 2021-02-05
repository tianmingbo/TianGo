# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 21:33
# @Author  : tmb
import collections

ct = collections.Counter('adjkahfjahfa')  # 只能给可散列表对象计数
print(ct)
ct.update('adjkfjakl')
print(ct)
print(ct.most_common(2))  # 按照次序返回映射里最常见的n个键和他们的计数
