# -*- coding: utf-8 -*-

import re
import subprocess

import requests
import execjs

node = execjs.get()

sum_comments = 0
restaurant_num = 0

session = requests.session()

headers = {
    'User-Agent': 'yuanrenxue.project'
}


def get_m():
    res = session.get('https://match.yuanrenxue.com/match/9', headers=headers)
    try:
        m = re.findall('for\(var\sm=0x1;m<=(\d);m\+\+\)', res.text)[0]
    except IndexError:
        m = re.findall('\(m,(\d)\);m\+\+\)', res.text)[0]
    decrypt_time = re.findall('decrypt,\'(\d{10})', res.text)[0]
    return m, decrypt_time


def get_page_info():
    global sum_comments, restaurant_num
    url = 'https://match.yuanrenxue.com/api/match/9?'
    iter_num, decrypt_time = get_m()
    p = subprocess.Popen(['node', './final_udc.js', iter_num, decrypt_time], stdout=subprocess.PIPE)
    m = p.stdout.read().decode('UTF-8').replace('\n', '')
    cookies = {
        'm': iter_num + str(m) + 'r'
    }
    print(cookies)
    for i in range(1, 6):
        res = session.get(f'{url}page={i}', headers=headers, cookies=cookies).json()
        for val in res['data']:
            sum_comments += val['value']
            restaurant_num += 1


if __name__ == '__main__':
    get_m()
    get_page_info()
    print(sum_comments / restaurant_num)
