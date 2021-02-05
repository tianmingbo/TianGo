# -*- coding: utf-8 -*-
# @Time    : 2020/11/12 10:30
# @Author  : tmb
# psutil:获取系统信息模块，可以获取CPU，内存，磁盘等的使用情况
import psutil
import time
import datetime


# logfile：监测信息写入文件
def MonitorSystem(logfile=None):
    # 获取cpu使用情况
    cpuper = psutil.cpu_percent()
    # 获取内存使用情况：系统内存大小，使用内存，有效内存，内存使用率
    mem = psutil.virtual_memory()
    # 内存使用率
    memper = mem.percent
    # 获取当前时间
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} cpu:{cpuper}%, mem:{memper}%'
    print(line)
    if logfile:
        logfile.write(line)


def MonitorNetWork(logfile=None):
    # 获取网络收信息
    netinfo = psutil.net_io_counters()
    # 获取当前时间
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} bytessent={netinfo.bytes_sent}, bytesrecv={netinfo.bytes_recv}'
    print(line)
    if logfile:
        logfile.write(line)


# 通过sleep，实现定时任务
def loopMonitor():
    while True:
        MonitorSystem()
        MonitorNetWork()
        # 2s检查一次
        time.sleep(3)

if __name__ == '__main__':
    # loopMonitor()
    pass
