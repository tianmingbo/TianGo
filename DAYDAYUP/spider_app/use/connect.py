import uiautomator2 as u2

# 通过usb连接，需要添加识别码
d = u2.connect_usb('3HX7N17118015052')
print(d.device_info)

# 也可以通过wifi连接

# adb-wifi
# d=u2.connect_adb_wifi()

# 启动app，首先通过aapt获取包名，然后启动app
# d.app_start('com.xunmeng.pinduoduo')
# d.uiautomator.start()  # 启动uiautomator
# print(d.uiautomator.running())
# d.uiautomator.stop()
# print(d.agent_alive)

# 查看窗口大小
print(d.window_size())

# 获取ip
print(d.wlan_ip)
