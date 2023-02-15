import execjs
import requests

headers = {
    "user-agent": "yuanrenxue,project",
}


def get_page_info():
    res = []
    with open('3.finally.js', 'r', encoding='utf-8') as f:
        encrypt = f.read()
    for page_num in range(1, 6):
        params = execjs.compile(encrypt).call('getParams')
        params = {
            "m": params['m'],
            "q": params['q']
        }
        url = f"https://match.yuanrenxue.com/api/match/6?page={page_num}"
        response = requests.get(url, headers=headers, params=params).json()
        for value in response['data']:
            res.append(value['value'])
        print(res)

    print(sum(res)*24)


if __name__ == '__main__':
    get_page_info()
