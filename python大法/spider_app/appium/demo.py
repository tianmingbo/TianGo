# @Time : 2022/4/7 21:14
# @Author :bo~
# @FileName: demo.py
# @Description: 使用appium驱动app
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

server = 'http://127.0.0.1:4723/wd/hub'
desired_capabilities = {
    "platformName": "Android",
    "appium:deviceName": "MHA_AL00",
    "appium:appPackage": "com.yaya.zone",
    "appium:appActivity": ".home.HomeActivity",
    "appium:noReset": True
}
driver = webdriver.Remote(server, desired_capabilities)
wait = WebDriverWait(driver, 30)

# el1 = driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/ani_car")
# el1.click()
# time.sleep(0.3)
# driver.swipe(496, 733, 474, 1382, 1000)  # 屏幕滑动
#
# print('click')
# el2 = driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/btn_submit")
# el2.click()
time.sleep(10)
try_count = 0
while True:
    try:
        driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/tv_submit")
        break
    except Exception:
        time.sleep(1)
while try_count < 100000000:
    try:
        el3 = driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/tv_submit")
        print('???')
        el3.click()
        driver.tap([(725, 976 + try_count % 9 * 100), ], 100)
        print(f'click(725,{976 + try_count % 9 * 100})')
        try_count += 1
    except Exception as e:
        print('error')
        time.sleep(0.01)
        try:
            driver.tap([(962, 663), ], 200)
        except Exception:
            pass
