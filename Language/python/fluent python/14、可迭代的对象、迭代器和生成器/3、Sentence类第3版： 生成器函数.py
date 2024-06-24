import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __iter__(self):
        for word in self.words:
            yield word  # 使用生成器，生成全部值后直接退出

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


'''
生成器函数：yield
调用生成器函数，会生成一个生成器对象。

'''


def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')


if __name__ == '__main__':
    obj = Sentence('tian is a good man!')
    for i in obj:
        print(i)
    for i in gen_AB():
        print(i)
