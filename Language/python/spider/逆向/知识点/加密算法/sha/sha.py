# @Time : 2022/5/23 23:20
# @Author :bo~
# @FileName: sha.py
# @Description:
import hashlib


def sha1_test1():
    sha1 = hashlib.new('sha1', 'I love chendali!'.encode('utf-8'))
    print(sha1.hexdigest())


def sha1_test2():
    sha1 = hashlib.sha1()
    sha1.update('I love chendali!'.encode('utf-8'))
    print(sha1.hexdigest())


if __name__ == '__main__':
    sha1_test1()  # 23c02b203bd2e2ca19da911f1d270a06d86719fb
    sha1_test2()  # 23c02b203bd2e2ca19da911f1d270a06d86719fb
