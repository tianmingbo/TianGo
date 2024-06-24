# # -*- coding: utf-8 -*-
# # @Time    : 2020/11/12 10:43
# # @Author  : tmb
# '''
# Timer方法说明Timer(interval, function, args=None, kwargs=None)创建定时器； cancel()取消定时器 ；start()使用线程方式执行 ；join(self, timeout=None)等待线程执行结束。
#
# 定时器只能执行一次，如果需要重复执行，需要重新添加任务；
# '''
# import datetime
# import psutil
#
# from threading import Timer
#
#
# # logfile：监测信息写入文件
# def MonitorSystem(logfile=None):
#     # 获取cpu使用情况
#     cpuper = psutil.cpu_percent()
#     # 获取内存使用情况：系统内存大小，使用内存，有效内存，内存使用率
#     mem = psutil.virtual_memory()
#     # 内存使用率
#     memper = mem.percent
#     # 获取当前时间
#     now = datetime.datetime.now()
#     ts = now.strftime('%Y-%m-%d %H:%M:%S')
#     line = f'{ts} cpu:{cpuper}%, mem:{memper}%'
#     print(line)
#     if logfile:
#         logfile.write(line)
#
#
# def MonitorNetWork(logfile=None):
#     # 获取网络收信息
#     netinfo = psutil.net_io_counters()
#     # 获取当前时间
#     now = datetime.datetime.now()
#     ts = now.strftime('%Y-%m-%d %H:%M:%S')
#     line = f'{ts} bytessent={netinfo.bytes_sent}, bytesrecv={netinfo.bytes_recv}'
#     print(line)
#     if logfile:
#         logfile.write(line)
#
#
# if __name__ == '__main__':
#     # 记录当前时间
#     print(datetime.datetime.now())
#     # 3S执行一次
#     sTimer = Timer(3, MonitorSystem)
#     # 1S执行一次
#     nTimer = Timer(1, MonitorNetWork)
#     # 使用线程方式执行
#     sTimer.start()
#     nTimer.start()
#     # 等待结束
#     sTimer.join()
#     nTimer.join()
#     # 记录结束时间
#     print(datetime.datetime.now())


from threading import Timer
import psutil
import time
import datetime


def MonitorSystem(logfile=None):
    cpuper = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    memper = mem.percent
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} cpu:{cpuper}%, mem:{memper}%'
    print(line)
    if logfile:
        logfile.write(line)
    # 启动定时器任务，每三秒执行一次
    Timer(3, MonitorSystem).start()


def MonitorNetWork(logfile=None):
    netinfo = psutil.net_io_counters()
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} bytessent={netinfo.bytes_sent}, bytesrecv={netinfo.bytes_recv}'
    print(line)
    if logfile:
        logfile.write(line)
    # 启动定时器任务，每秒执行一次
    Timer(1, MonitorNetWork).start()


MonitorSystem()
MonitorNetWork()
