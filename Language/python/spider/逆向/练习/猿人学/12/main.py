import base64
import requests

sum_num = 0
session = requests.session()


def login():
    data = {
        'username': '********',
        'password': '********'
    }
    session.post('https://match.yuanrenxue.com/api/login', data=data)
    session.get('https://match.yuanrenxue.com/api/loginInfo')


def get_page_info():
    global sum_num
    url = 'https://match.yuanrenxue.com/api/match/12?'
    for i in range(1, 6):
        params = {
            'page': i,
            'm': base64.b64encode(f'yuanrenxue{i}'.encode())
        }
        res = session.get(url, headers={'User-Agent': 'yuanrenxue.project'}, params=params)
        res = res.json()
        for val in res['data']:
            sum_num += val['value']


if __name__ == '__main__':
    login()
    get_page_info()
    print(sum_num)
