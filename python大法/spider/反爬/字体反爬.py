import re

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from pyquery import PyQuery as pq

ser = Service("../chromedriver.exe")
TIMEOUT = 10


def parse_score(item):
    # 首先建立CSS映射
    css_url = 'https://antispider4.scrape.center/css/app.654ba59e.css'
    response = requests.get(css_url)
    results = re.findall(re.compile('.icon-(\d+):before\{content:"(.*?)"\}'), response.text)
    icon_map = {item[0]: item[1] for item in results}
    elements = item('.icon')
    icon_values = []
    for element in elements.items():
        class_name = element.attr('class')
        icon_key = re.search(r'icon-(\d+)', class_name).group(1)
        icon_value = icon_map.get(icon_key)
        icon_values.append(icon_value)
    return ''.join(icon_values)


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(service=ser, options=options)
wait = WebDriverWait(browser, TIMEOUT)

browser.get('https://antispider4.scrape.center/')
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item')))
html = browser.page_source
doc = pq(html)
items = doc('.item')
for item in items.items():
    name = item('.name').text()
    categories = [o.text() for o in item('.categories button').items()]
    score = parse_score(item)
    print(name, categories, score)
browser.close()
