import math
import random
import time
import pywasm
import requests

sum_num = 0

session = requests.session()


def get_wasm():
    response = requests.get('https://match.yuanrenxue.com/static/match/match15/main.wasm')
    with open('main.wasm', 'wb') as f:
        f.write(response.content)


def login():
    data = {
        'username': 'chendali',
        'password': '******'
    }
    session.post('https://match.yuanrenxue.com/api/login', data=data)
    session.get('https://match.yuanrenxue.com/api/loginInfo')


def get_page_info():
    global sum_num
    wasm = pywasm.load("main.wasm")
    url = 'https://match.yuanrenxue.com/api/match/15?'
    for i in range(1, 6):
        t = time.time()
        t1 = int(t / 2)
        t2 = int(t / 2 - math.floor(random.random() * 50 + 1))
        params = {
            'm': f'{wasm.exec("encode", [t1, t2])}|{t1}|{t2}',
            'page': i
        }
        res = session.get(f'{url}page={i}', headers={'User-Agent': 'yuanrenxue.project'}, params=params)
        res = res.json()
        for val in res['data']:
            sum_num += val['value']


if __name__ == '__main__':
    login()
    get_wasm()
    get_page_info()
    print(sum_num)
