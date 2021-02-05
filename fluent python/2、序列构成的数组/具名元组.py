# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 23:12
# @Author  : tmb
from collections import namedtuple

City = namedtuple('City', 'name country population coordinates')

china = City('beijing', 'China', 13, (30, 120))
print(china.name)
print(china.country)

print(City._fields) #输出属性
print(City._make(('shanghai', 'China', 13, (30, 120)))) #生成实例
print(china._asdict())