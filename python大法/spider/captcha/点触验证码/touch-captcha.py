import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from chaojiying import ChaoJiYingClient

EMAIL = 'test'
PASSWORD = 'test'


class CrackGeetest():
    s = Service(r'../../chromedriver.exe')

    def __init__(self):
        self.url = 'https://www.geetest.com/demo/click-popup-en.html'
        self.browser = webdriver.Chrome(service=self.s)
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = ChaoJiYingClient('chendali', '********', '928872')  # 用户中心>>软件ID 生成一个替换

    def crack(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()
        self.get_captcha('captcha.png')
        res = self.chaojiying.PostPic(open('captcha.png', 'rb').read(), 9005)
        print(res)
        locations = self.get_locations(res)
        self.touch_click_words(locations)
        self.click_submit()
        time.sleep(10)

    @staticmethod
    def get_locations(captcha_result):
        """
        解析识别结果,得到坐标
        :param captcha_result:
        :return:
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def get_touch_element(self):
        """
        获取验证码对象
        :return:
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_widget')))
        return element

    def click_submit(self):
        # 点击提交按钮
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_commit')))
        element.click()
        print('success')

    def touch_click_words(self, locations):
        """
        点击坐标
        :param locations:
        :return:
        """
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touch_element(), location[0],
                                                                   location[1]).click().perform()
            time.sleep(0.5)

    def __del__(self):
        self.browser.close()

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        # element_to_be_clickable是否可点击
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_captcha(self, name):
        img = self.get_touch_element()
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        screenshot = self.get_screenshot()
        order_words_img = screenshot.crop((left, top, right, bottom))
        order_words_img.save(name)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(
            EC.presence_of_element_located((By.ID, 'username')))  # presence_of_element_located检查页面上是否存在元素
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        username.send_keys(self.email)
        password.send_keys(self.password)


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()
