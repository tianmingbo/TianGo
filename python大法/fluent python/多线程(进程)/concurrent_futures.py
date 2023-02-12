"""
future：
future封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果后（或抛出异常）可以查看结果（异常）。
未来对象，task的返回容器
"""
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
from concurrent.futures import Future

# 线程池， 为什么要线程池
# 主线程中可以获取某一个线程的状态或者某一个任务的状态，以及返回值
# 当一个线程完成的时候我们主线程能立即知道
# futures可以让多线程和多进程编码接口一致
import time


def get_html(times):
    time.sleep(times)
    print("get page {} success".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中, submit 是立即返回
# task1 = executor.submit(get_html, (3))
# task2 = executor.submit(get_html, (2))


# 要获取已经成功的task的返回
urls = [3, 2, 4]
all_task = [executor.submit(get_html, (url)) for url in urls]  # 为传入的可调用对象get_html排期，并返回一个future
# wait(all_task, return_when=FIRST_COMPLETED)
# print("main")
for future in as_completed(all_task):  # as_completed 参数是一个future列表,返回值是一个迭代器
    data = future.result()
    print("get {} page".format(data))
# 通过executor的map获取已经完成的task的值
# for data in executor.map(get_html, urls):
#     print("get {} page".format(data))


# #done方法用于判定某个任务是否完成
# print(task1.done())
# print(task2.cancel())
# time.sleep(3)
# print(task1.done())
#
# #result方法可以获取task的执行结果
# print(task1.result())
