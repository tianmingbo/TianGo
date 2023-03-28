import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from services.common import chaojiying
from services.base_service import BaseService


class ZhihuLoginService(BaseService):
    name = "zhihu"

    def __init__(self, settings):
        self.user_name = settings.Accounts[self.name]["username"]
        self.pass_word = settings.Accounts[self.name]["password"]
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser = webdriver.Chrome(executable_path="D:/c盘下载/chromedriver.exe",
                                   options=chrome_options)

    def check_login(self):
        try:
            self.browser.find_element_by_css_selector(".Popover.PushNotifications.AppHeader-notifications")
            return True
        except Exception as e:
            return False

    def check_cookie(self, cookie_dict):
        res = requests.get("https://www.zhihu.com/", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
        }, cookies=cookie_dict, allow_redirects=False)
        if res.status_code != 200:
            return False
        else:
            return True

    def login(self):
        import time
        try:
            self.browser.maximize_window()  # 将窗口最大化防止定位错误
        except Exception as e:
            pass

        while not self.check_login():
            self.browser.get("https://www.zhihu.com/signin")

            #选择用户密码登陆元素并点击
            time.sleep(5)
            login_element = self.browser.find_element_by_css_selector(".SignFlow-tabs div.SignFlow-tab")
            login_element.click()

            browser_navigation_panel_height = self.browser.execute_script('return window.outerHeight - window.innerHeight;')
            time.sleep(5)

            self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
            self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                self.user_name)

            self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
            self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                self.pass_word)

            self.browser.find_element_by_css_selector(
                ".Button.SignFlow-submitButton").click()
            time.sleep(15)
            from mouse import move, click

            print("判断登录是否成功")
            if self.check_login():
                break
            try:
                # 查询是否有英文验证码
                english_captcha_element = self.browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_element = None
            try:
                # 查询是否有中文验证码
                chinese_captcha_element = self.browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_element = None

            if chinese_captcha_element:
                y_relative_coord = chinese_captcha_element.location['y']
                y_absolute_coord = y_relative_coord + browser_navigation_panel_height
                x_absolute_coord = chinese_captcha_element.location['x']

                """
                保存图片
                1. 通过保存base64编码
                2. 通过crop方法
                """
                # 1. 通过保存base64编码
                base64_text = chinese_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_cn.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                from zheye import zheye
                z = zheye()
                positions = z.Recognize("yzm_cn.jpeg")

                pos_arr = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        pos_arr.append([positions[1][1], positions[1][0]])
                        pos_arr.append([positions[0][1], positions[0][0]])
                    else:
                        pos_arr.append([positions[0][1], positions[0][0]])
                        pos_arr.append([positions[1][1], positions[1][0]])
                else:
                    pos_arr.append([positions[0][1], positions[0][0]])

                if len(positions) == 2:
                    first_point = [int(pos_arr[0][0] / 2), int(pos_arr[0][1] / 2)]
                    second_point = [int(pos_arr[1][0] / 2), int(pos_arr[1][1] / 2)]

                    move((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    click()

                    move((x_absolute_coord + second_point[0]), y_absolute_coord + second_point[1])
                    click()

                else:
                    first_point = [int(pos_arr[0][0] / 2), int(pos_arr[0][1] / 2)]

                    move((x_absolute_coord + first_point[0]), y_absolute_coord + first_point[1])
                    click()

                self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    self.user_name)

                self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                    self.pass_word)
                self.browser.find_element_by_css_selector(
                    ".Button.SignFlow-submitButton").click()
                self.browser.find_element_by_css_selector(
                    ".Button.SignFlow-submitButton").click()

            if english_captcha_element:
                # 2. 通过crop方法
                # from pil import Image
                # image = Image.open(path)
                # image = image.crop((locations["x"], locations["y"], locations["x"] + image_size["width"],
                #                     locations["y"] + image_size["height"]))  # defines crop points
                #
                # rgb_im = image.convert('RGB')
                # rgb_im.save("D:/ImoocProjects/python_scrapy/coding-92/ArticleSpider/tools/image/yzm.jpeg",
                #             'jpeg')  # saves new cropped image
                # # 1. 通过保存base64编码
                base64_text = english_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
                # print code
                fh = open("yzm_en.jpeg", "wb")
                fh.write(base64.b64decode(code))
                fh.close()

                cjy_cli = chaojiying.Chaojiying_Client(settings.CJY_USERNAME, settings.CJY_PASSWORD, '96001')
                im = open("yzm_en.jpeg", 'rb').read()
                json_data = cjy_cli.PostPic(im, 1902)
                if json_data["err_no"] == 0:
                    print("识别成功！")
                    code = json_data["pic_str"]
                    print("英文验证码： {code}".format(code=code))
                else:
                    print("识别失败，继续尝试！")
                    return

                self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                self.browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(code)

                self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + "a")
                self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    self.user_name)

                self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
                    self.pass_word)
                submit_ele = self.browser.find_element_by_css_selector(".Button.SignFlow-submitButton")
                self.browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()

            # 等待登录成功后加载个人中心信息
            time.sleep(10)

        Cookies = self.browser.get_cookies()
        print(Cookies)
        cookie_dict = {}
        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        self.browser.close()
        return cookie_dict


if __name__ == "__main__":
    import settings
    zhihu = ZhihuLoginService(settings)
    cookie_dict = zhihu.login()
    print(cookie_dict)

    import requests
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }
    rsp = requests.get("https://www.zhihu.com/", headers=headers, cookies=cookie_dict, allow_redirects=False)
    print(rsp.status_code)
    # print(rsp.text)
