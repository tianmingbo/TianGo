import time

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

setting = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.ss.android.ugc.aweme",
    "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
    "noReset": True,
    "unicodekeyboard": True,
    "resetkeyboard": True
}
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", setting)  # 连接服务器

# 点击我
try:
    while WebDriverWait(driver, 15).until(lambda x: x.find_element_by_xpath(
            '//*[@resource-id="com.ss.android.ugc.aweme:id/d3z"]/android.widget.FrameLayout[5]')):
        time.sleep(12)
        driver.tap([(363, 702), (363, 702)], 500)
        driver.find_element_by_xpath(
            '//*[@resource-id="com.ss.android.ugc.aweme:id/d3z"]/android.widget.FrameLayout[5]').click()
except:
    pass

# 点击关注
try:
    while WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/bsf"]')):
        driver.find_element_by_xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/bsf"]').click()
except:
    pass

# 点击头像
try:
    while WebDriverWait(driver, 5).until(
            lambda x: x.find_element_by_xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/db1"]')):
        driver.find_element_by_xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/db1"]').click()
except:
    pass

# 点击头像
try:
    while WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/fqm"]')):
        driver.find_element_by_xpath('//*[@resource-id="com.ss.android.ugc.aweme:id/fqm"]').click()
except:
    pass
