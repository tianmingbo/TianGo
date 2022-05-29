# @Time : 2022/5/23 23:18
# @Author :bo~
# @FileName: md5.py
# @Description:
import hashlib
import sys
import hashlib


def md5_test1():
    md5 = hashlib.new('md5', 'I love python!'.encode('utf-8'))
    print(md5.hexdigest())


def md5sum():
    with open('tmp.txt', 'rb', encoding='utf-8') as f:
        file_md5 = hashlib.md5(f.read()).hexdigest()
    return file_md5


def get_file_md5(fname):
    """
    获取file的md5值
    :param fname:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象

    return m.hexdigest()  # 返回md5对象


def md5_test2():
    md5 = hashlib.md5()
    md5.update('I love '.encode('utf-8'))
    md5.update('python!'.encode('utf-8'))
    print(md5.hexdigest())


if __name__ == '__main__':
    md5_test1()  # 21169ee3acd4a24e1fcb4322cfd9a2b8
    md5_test2()  # 21169ee3acd4a24e1fcb4322cfd9a2b8
    print(get_file_md5('tmp.txt'))
    print(get_file_md5('22.txt'))
