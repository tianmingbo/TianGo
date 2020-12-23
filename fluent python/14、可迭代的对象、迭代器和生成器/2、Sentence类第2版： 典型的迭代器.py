# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 22:50
# @Author  : tmb
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self):
        return SentenceIterator(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # 缩略表示


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        # 迭代器实现__next__和__iter__方法
        try:
            word = self.words[self.index]
        except StopIteration:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self
