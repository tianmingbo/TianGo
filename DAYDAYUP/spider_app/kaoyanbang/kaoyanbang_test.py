# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 16:27
# @Author  : tmb
# pip install Appium-ython-Client

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

tmp = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.tal.kaoyan",
    "appActivity": "com.tal.kaoyan.ui.activity.SplashActivity",
    "noReset": True
}

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", tmp)
driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tip_commit']").click()
try:
    if WebDriverWait(driver, 6).until(
            lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_skip']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_skip']").click()
except:
    pass
driver.find_element_by_xpath(
    "//android.widget.EditText[@resource-id='com.tal.kaoyan:id/kylogin_phone_input_phonenum']").send_keys('18848868890')
driver.find_element_by_xpath(
    "//android.widget.TextView[@resource-id='com.tal.kaoyan:id/kylogin_phone_input_codeget']").click()

# driver.swipe()  # 鼠标滑动坐标
