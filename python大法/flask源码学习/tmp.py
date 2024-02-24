from werkzeug.local import LocalStack

# 创建一个本地堆栈对象
my_stack = LocalStack()


# 在线程中设置变量值
def worker():
    my_stack.push('foo')
    print(my_stack.top)  # 输出: foo
    my_stack.pop()


# 在多个线程中调用 worker 函数
import threading

thread1 = threading.Thread(target=worker)
thread2 = threading.Thread(target=worker)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
