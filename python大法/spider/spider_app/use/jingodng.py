import time

import uiautomator2 as u2

d = u2.connect_usb()
d.press('home')
if not d(text="京东").exists:
    d.swipe_ext('left')
d(text="京东").click()
time.sleep(0.5)
d.xpath(
    '//*[@resource-id="com.jingdong.app.mall:id/y7"]/androidx.recyclerview.widget.RecyclerView[1]/android.widget.RelativeLayout[7]')
