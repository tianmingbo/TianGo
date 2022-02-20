from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

ser = Service("../../chromedriver.exe")

option = ChromeOptions()
# 88版本已失效
option.add_experimental_option('excludeSwitches', ['enabled-automation'])

option.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(service=ser, options=option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                        {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined}})'})
browser.get('https://antispider1.scrape.center/')
