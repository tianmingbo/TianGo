# @Time : 2022/4/20 21:49
# @Author :bo~
# @FileName: demo.py
# @Description:
from scrapy import Selector


# selector 支持xpath，css，re

class Test:
    def __init__(self):
        self.name = 'test'

    def parse(self):
        print(self.__class__.__dict__)


if __name__ == '__main__':
    a = Test()
    a.parse()
