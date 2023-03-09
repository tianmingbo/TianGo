import requests
import execjs
import time
from urllib.parse import quote
import urllib

node = execjs.get()
with open('1.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())

sum_price, count = 0, 0


def get_page_info():
    global sum_price, count
    url = 'https://match.yuanrenxue.com/api/match/1?'
    for i in range(1, 6):
        _time = int(time.time()) * 1000 + 100000000
        params = {
            'page': i,
            'm': ctx.eval(f'getM("{_time}")') + '丨' + f'{_time // 1000}'
        }
        time.sleep(0.5)
        query_string = urllib.parse.urlencode(params)
        res = requests.get(url + query_string, headers={'User-Agent': 'yuanrenxue.project'}).json()
        print(res)
        for val in res['data']:
            count += 1
            sum_price += val['value']
        # break


if __name__ == '__main__':
    get_page_info()
    print(sum_price / count)
