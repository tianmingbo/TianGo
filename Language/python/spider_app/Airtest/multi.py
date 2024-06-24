# @Time : 2022/4/11 21:29
# @Author :bo~
# @FileName: multi.py
# @Description: 群控手机
import adbutils
from airtest.core.api import *
from multiprocessing import Process
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

PACKAGE_NAME = 'com.goldze.mvvmhabit'
APK_PATH = 'scrape-app5.apk'


class Controller(object):
    def __init__(self, device_uri, package_name, apk_path, need_reinstall=False, need_restart=False):
        self.device_uri = device_uri
        self.package_name = package_name
        self.apk_path = apk_path
        self.need_reinstall = need_reinstall
        self.need_restart = need_restart

    def connect_device(self):
        self.device = connect_device(self.device_uri)

    def install_app(self):
        if self.device.check_app(self.package_name) and not self.need_reinstall:
            return
        self.device.uninstall_app(self.package_name)
        self.device.install_app(self.apk_path)

    def start_app(self):
        if self.need_restart:
            self.device.stop_app(self.package_name)
        self.device.start_app(self.package_name)

    def scroll_up(self):
        # 滑动
        self.device.swipe((self.window_width * 0.5, self.window_height * 0.8),
                          (self.window_width * 0.5, self.window_height * 0.3), duration=1)

    def init_device(self):
        # 初始化
        self.connect_device()  # 连接设备
        self.poco = AndroidUiautomationPoco(self.device)
        self.window_width, self.window_height = self.poco.get_screen_size()
        self.install_app()
        self.start_app()

    def run(self):
        for _ in range(10):
            self.scroll_up()
        self.device.stop_app(self.package_name)


def run(device_uri):
    controller = Controller(device_uri=device_uri,
                            package_name=PACKAGE_NAME,
                            apk_path=APK_PATH,
                            need_reinstall=False,
                            need_restart=True)
    controller.init_device()
    controller.run()


if __name__ == '__main__':
    # 多进程实现手机群控
    processes = []
    adb = adbutils.AdbClient('127.0.0.1', port=5037)
    # 获取所有手机列表
    for device in adb.device_list():
        print(device)
        device_name = device.serial
        device_uri = f'Android:///{device_name}'
        p = Process(target=run, args=(device_uri,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
