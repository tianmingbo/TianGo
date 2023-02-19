import base64
import re

import requests

sum_num = 0
session = requests.session()


def login():
    data = {
        'username': 'chendali',
        'password': '********'
    }
    session.post('https://match.yuanrenxue.com/api/login', data=data)
    session.get('https://match.yuanrenxue.com/api/loginInfo')


def get_page_info():
    global sum_num
    response = session.get('https://match.yuanrenxue.com/match/13')
    cookies = {
        'yuanrenxue_cookie': ''.join(re.findall('\(\'(.)\'\)', response.text)).split('=')[1]
    }
    url = 'https://match.yuanrenxue.com/api/match/13?'
    for i in range(1, 6):
        res = session.get(f'{url}page={i}', headers={'User-Agent': 'yuanrenxue.project'}, cookies=cookies)
        print(res.text)
        res = res.json()
        for val in res['data']:
            sum_num += val['value']


if __name__ == '__main__':
    login()
    get_page_info()
    print(sum_num)
