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

el1 = driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/ani_car")
el1.click()
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(770, 1830)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.move_to_location(496, 733)
actions.w3c_actions.pointer_action.release()
actions.perform()

actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(482, 759)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.move_to_location(474, 1382)
actions.w3c_actions.pointer_action.release()
actions.perform()

print('click')
el2 = driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/btn_submit")
el2.click()
time.sleep(1)
try_count = 0

while try_count < 100000000:
    try:
        el3 = driver.find_element(by=AppiumBy.ID, value="com.yaya.zone:id/tv_submit")
        print('???')
        el3.click()
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(725, 976 + try_count % 9 * 100)
        # actions.w3c_actions.pointer_action.move_to_location(694, 516)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print(f'click(725,{976 + try_count % 9 * 100})')
        try_count += 1
    except Exception as e:
        print('error')
        time.sleep(0.01)
        try:
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(962, 663)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
        except Exception as e:
            print('none')
