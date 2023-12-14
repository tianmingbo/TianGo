import time
from multiprocessing import Process
from threading import Thread


def count(to: int):
    start = time.perf_counter()
    counter = 0
    while counter < to:
        counter += 1
    end = time.perf_counter()

    print(f"在 {end - start} 秒内将 counter 增加到 {to}")


if __name__ == '__main__':
    print('multiProcess')
    start = time.perf_counter()
    task1 = Process(target=count, args=(100000000,))
    task2 = Process(target=count, args=(100000000,))
    # 启动进程
    task1.start()
    task2.start()
    # 该方法会一直阻塞主进程，直到子进程执行完成，并且 join 方法内部也可以接收一个超时时间
    # 如果子进程在规定时间内没有完成，那么主进程不再等待
    task1.join()
    task2.join()
    end = time.perf_counter()
    print(f"在 {end - start} 秒内完成")
    # multiThread
    # 因为GIL的原因，并没有提升效率
    print('multiThread')
    start = time.perf_counter()
    # 多线程和多进程相关的 API 是一致的，只需要将 Process 换成 Thread 即可
    task1 = Thread(target=count, args=(100000000,))
    task2 = Thread(target=count, args=(100000000,))
    task1.start()
    task2.start()
    task1.join()
    task2.join()
    end = time.perf_counter()
    print(f"在 {end - start} 秒内完成")
