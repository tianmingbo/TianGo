# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 22:24
# @Author  : tmb
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __len__(self):
        return len(self.words)

    def __getitem__(self, item):  # get或者索引使用
        return self.words[item]

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # 缩略表示


'''
序列可以迭代的原因： iter函数
解释器需要迭代对象 x 时，会自动调用 iter(x)。
内置的 iter 函数有以下作用。
(1) 检查对象是否实现了 __iter__ 方法，如果实现了就调用它，获取一个迭代器。
(2) 如果没有实现 __iter__ 方法，但是实现了 __getitem__ 方法， Python 会创建一个迭代
器，尝试按顺序（从索引 0 开始）获取元素。
(3) 如果尝试失败， Python 抛出 TypeError 异常，通常会提示“C object is not iterable”（C
对象不可迭代），其中 C 是目标对象所属的类。
任何 Python 序列都可迭代的原因是，它们都实现了 __getitem__ 方法。
'''

if __name__ == '__main__':
    a = Sentence('tian ming bo is a good man! tian ming bo is a good man! tian ming bo is a good man!')
    print(Sentence.__dict__)
    print(len(a))
    print(a)
    print(a[1])
