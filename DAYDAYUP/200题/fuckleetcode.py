# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 14:45
# @Author  : tmb
from selenium import webdriver
from lxml import etree
import time

'''
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"  手动启浏览器
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(chrome_options=chrome_options)  # 创建Chrome对象.


def get_all_links():
    # 进入浏览器设置

    driver.get('https://leetcode-cn.com/problemset/leetcode-200/')
    # html = etree.HTML(driver.page_source)
    #
    # driver.find_element_by_xpath('//div[@class="css-lzlnnl-primary-title-AuthLinks ergbin812"]//a[2]').click()
    # time.sleep(1)
    #
    # driver.find_element_by_xpath('//div[@data-cypress="sign-in-with-password"]').click()
    #
    # driver.find_element_by_xpath('//input[@placeholder="手机号/邮箱"]').send_keys('+19787688589')
    # driver.find_element_by_xpath('//input[@placeholder="输入密码"]').send_keys('qqq123456')
    # driver.find_element_by_xpath('//button[@type="submit"]/span').click()
    # time.sleep(10)
    time.sleep(1)
    html = etree.HTML(driver.page_source)
    links = html.xpath('//div[@class="question-title"]/a/@href')
    links_2 = []
    for i in range(len(links)):
        links_2.append('https://leetcode-cn.com' + links[i])
    return links_2


def get_one_info(link):
    driver.get(link)
    time.sleep(1)
    html = etree.HTML(driver.page_source)
    page = html.xpath('//div[@class="description__2b0C"]')
    try:
        content = etree.tostring(page[0])
    except:
        return
    name = html.xpath('//h4[@data-cypress="QuestionTitle"]/a/text()')[0] + '.html'
    with open(name, 'w+') as f:
        f.write('''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Title</title>
        </head>
        <body>
        ''')
        f.write(content.decode('ascii'))
        f.write('''</body>
        </html>
        ''')
    print(content.decode('ascii'))


if __name__ == '__main__':
    links = get_all_links()
    print(links)
    for i in links:
        get_one_info(i)
        time.sleep(1.5)
