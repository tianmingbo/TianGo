import subprocess
import time
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
    url = 'https://match.yuanrenxue.com/match/18data?'
    for i in range(1, 6):
        t = str(int(time.time()))
        p = subprocess.Popen(['/usr/local/bin/node', './jsvmp.js', t, str(i)], stdout=subprocess.PIPE)
        v = p.stdout.read().decode('UTF-8').replace('\n', '')
        params = {'page': i}
        if i != 1:
            params['v'] = v
            params['t'] = t
        print(params)
        res = session.get(f'{url}page={i}', headers={'User-Agent': 'yuanrenxue.project'}, params=params)
        print(res.text)
        res = res.json()
        for val in res['data']:
            sum_num += val['value']


if __name__ == '__main__':
    login()
    get_page_info()
    print(sum_num)
