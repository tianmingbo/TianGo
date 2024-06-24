import time
import requests
import execjs

sum_num = 0

session = requests.session()
node = execjs.get()
with open('webpack1.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())


def login():
    data = {
        'username': 'chendali',
        'password': '********'
    }
    session.post('https://match.yuanrenxue.com/api/login', data=data)
    session.get('https://match.yuanrenxue.com/api/loginInfo')


def get_page_info():
    global sum_num
    url = 'https://match.yuanrenxue.com/api/match/16?'
    for i in range(1, 6):
        t = str(int(time.time() * 1000))
        params = {
            'm': ctx.call('getM', t),
            'page': i,
            't': t
        }
        res = session.get(f'{url}page={i}', headers={'User-Agent': 'yuanrenxue.project'}, params=params)
        print(res.text)
        res = res.json()
        for val in res['data']:
            sum_num += val['value']


if __name__ == '__main__':
    login()
    get_page_info()
    print(sum_num)
