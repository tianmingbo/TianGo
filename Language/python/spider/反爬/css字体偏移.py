import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from pyquery import PyQuery as pq
import logging

ser = Service("../chromedriver.exe")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
TIMEOUT = 10

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(service=ser, options=options)
wait = WebDriverWait(browser, TIMEOUT)


def parse_name(content):
    has_whole = content('.whole')
    if has_whole:
        return content.text()
    chars = content('.char')
    items = []
    for char in chars.items():
        items.append({'text': char.text().strip(),
                      'left': int(re.search('(\d{0,3})px', char.attr('style')).group(1))
                      })
    items = sorted(items, key=lambda x: x['left'], reverse=False)  # 以偏移量排序，递增
    return ''.join([item.get('text') for item in items])


browser.get('https://antispider3.scrape.center/')
wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.item')))
html = browser.page_source
doc = pq(html)
names = doc('.item .name')
for name_html in names.items():
    name = parse_name(name_html)
    print(name)
browser.close()
