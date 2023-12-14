import multiprocessing
import time
from multiprocessing import Pool


def say_hello(name) -> str:
    time.sleep(2)
    return f"hello, {name}"


if __name__ == '__main__':
    print(multiprocessing.cpu_count())
    with Pool() as pool:
        hi1 = pool.apply(say_hello, args=("satori",))  # 串行
        hi2 = pool.apply(say_hello, args=("koishi",))
        print(hi1)
        print(hi2)
"""
hello, satori
hello, koishi
"""
