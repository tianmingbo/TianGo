# @Time : 2022/4/8 14:42
# @Author :bo~
# @FileName: demo.py
# @Description: airtest demo
from airtest.core.android import Android
from airtest.core.api import *
import logging

logging.getLogger('airtest').setLevel(logging.WARNING)
device: Android = init_device('Android')
is_locked = device.is_locked()  # 是否锁定
if is_locked:
    device.unlock()  # 解锁
device.wake()  # 唤醒当前设备
app_list = device.list_app()  # app列表
uuid = device.uuid
ip_address = device.get_ip_address()  # ip地址
top_activity = device.get_top_activity()  # 当前运行的activity
print(top_activity)


def all_devices():
    return G.DEVICE_LIST  # G是airtest中的一个全局变量，获取所有设备


print(all_devices())
exit()


@logwrap
def shell(cmd):
    return G.DEVICE.shell(cmd)  # 执行命令行


res = shell('cat /proc/meminfo')


@logwrap
def start_app(package_name, activity=None):
    G.DEVICE.start_app(package_name, activity)  # 启动app


@logwrap
def stop_app(package_name):
    G.DEVICE.stop_app(package_name)


package = 'com.tencent.mm'
start_app(package)
sleep(10)
stop_app(package)
# print(res)
