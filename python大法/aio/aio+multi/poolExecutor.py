from concurrent.futures import ThreadPoolExecutor
import time


def task(name, age, n):
    time.sleep(n)
    return f"name is {name}, age is {age}, sleep {n}s"


# 创建一个线程池，里面还可以指定 max_workers 参数，表示最多创建多少个线程
# 如果不指定，那么每一个任务都会为其创建一个线程
executor = ThreadPoolExecutor()

# 通过 submit 就直接将任务提交到线程池里面了，一旦提交，就会立刻运行
# 提交之后，相当于开启了一个新的线程，主线程会继续往下走
# 参数按照函数名，对应参数提交即可，切记不可写成 task("dali", 16, 3)，这样就变成调用了
futures = [executor.submit(task, "dali", 16, 3),
           executor.submit(task, "dali", 16, 4),
           executor.submit(task, "dali", 16, 1),
           ]
print(futures)  # <Future at 0x226b860 state=running>

# 让主程序也休眠 3s
time.sleep(3.1)

# 此时再打印
print(futures)  # <Future at 0x226b860 state=finished returned str>
print(futures[0].result())
"""
可以看到，一开始任务处于running，正在运行状态
3s 过后，任务处于 finished，完成状态，并告诉我们返回了一个 str
"""
