import requests
import execjs
import urllib

node = execjs.get()
with open('final.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())

sum_price = 0


def get_m():
    with open('final.js', 'r', encoding='utf8') as f:
        js = f.read()
    value = execjs.compile(js).call("getCookie")
    return value


def get_page_info():
    global sum_price
    url = 'https://match.yuanrenxue.com/api/match/2?'
    headers = {
        'User-Agent': 'yuanrenxue.project'
    }
    for i in range(1, 6):
        params = {
            'page': i
        }
        query_string = urllib.parse.urlencode(params)
        headers['cookie'] = get_m()
        res = requests.get(url + query_string, headers=headers).json()
        for val in res['data']:
            sum_price += val['value']


if __name__ == '__main__':
    get_page_info()
    print(sum_price)
