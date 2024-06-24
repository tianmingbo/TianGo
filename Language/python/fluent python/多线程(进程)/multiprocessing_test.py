import os

# fork只能用于linux/unix中
import time

# pid = os.fork()  # 创建一个子进程
# print("tian")
# if pid == 0:
#     print('子进程 {} ，父进程是： {}.'.format(os.getpid(), os.getppid()))
# else:
#     print('我是父进程：{}.'.format(pid))
# time.sleep(2)
import multiprocessing
from concurrent.futures import ProcessPoolExecutor  # 首选ProcessPoolExecutor
# 多进程编程
import time


def get_html(n):
    time.sleep(n)
    print("sub_progress success")
    return n


if __name__ == "__main__":
    # progress = multiprocessing.Process(target=get_html, args=(2,))
    # print(progress.pid)
    # progress.start()
    # print(progress.pid)
    # progress.join()
    # print("main progress end")

    # 使用进程池
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # result = pool.apply_async(get_html, args=(3,))
    #
    # # 等待所有任务完成
    # pool.close()  # 首先关闭
    # pool.join()
    #
    # print(result.get())  # 返回值

    # imap
    for result in pool.imap(get_html, [1, 5, 3]):
        print("{} sleep success".format(result))

    for result in pool.imap_unordered(get_html, [1, 5, 3]):
        print("{} sleep success".format(result))
