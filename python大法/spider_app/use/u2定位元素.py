import time

import uiautomator2 as u2

d = u2.connect_usb()

# 安装app，参数为apk地址
# d.app_install('https://t.alipayobjects.com/L1/71/100/and/alipay_wap_main.apk')

# d.app_start('com.tencent.tmgp.sgame')
# time.sleep(10)
# d.xpath('//android.widget.FrameLayout[1]').click()
# d(text="王者荣耀").click()
# d(resourceId="android:id/content").click()
# d.screen_off()
# d.screen_on()
# d.unlock()
# d.click(0.551, 0.907)
# d.click(0.168, 0.551)
# d.click(0.482, 0.584)
# d.click(0.85, 0.576)
# d.click(0.177, 0.681)
# d.click(0.532, 0.711)

# d.press('home')
# d.swipe_ext('right')  # 左滑
# d.swipe_ext('left')

d.swipe_points([])  # 滑动坐标
