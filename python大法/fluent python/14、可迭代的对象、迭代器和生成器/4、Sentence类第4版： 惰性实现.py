# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 16:59
# @Author  : tmb
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()


if __name__ == '__main__':
    a = Sentence('tian ming bo is a good man')
    for i in a:
        print(i)