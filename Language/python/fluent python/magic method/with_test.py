import contextlib


# 上下文管理器协议
class Sample:
    def __enter__(self):
        print("enter")
        # 获取资源
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        print("exit")

    def do_something(self):
        print("doing something")


with Sample() as sample:
    sample.do_something()

"""
enter
doing something
exit
"""


# 简化上下文管理器
@contextlib.contextmanager
def file_open(file_name):
    print("file open")
    yield {}
    print("file end")


with file_open("test.txt") as f_opened:
    print("file processing")
