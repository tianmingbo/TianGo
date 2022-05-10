# @Time : 2022/3/10 22:50
# @Author :bo~
# @FileName: demo.py
# @Description: 使用playwright模拟替换js文件，执行js逆向
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://spa2.scrape.center"
content = sync_playwright().start()
browser = content.chromium.launch(headless=False)
page = browser.new_page()
page.route("js/chunk-10192a00.243cb8b7.js", lambda route: route.fulfill(path='chunk.js'))  # 替换成本地文件
page.goto(BASE_URL)
