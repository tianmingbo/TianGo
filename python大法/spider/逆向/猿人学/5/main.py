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
        cookies = {
            "m": params['cookie_m'],
            "RM4hZBv0dDon443M": params['cookie_rm4']
        }
        params = {
            "m": params['m'],
            "f": params['f']
        }
        url = f"https://match.yuanrenxue.com/api/match/5?page={page_num}"
        response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
        for value in response['data']:
            res.append(value['value'])
    res.sort(reverse=True)
    print(res[:5], '\n', sum(res[:5]))


if __name__ == '__main__':
    get_page_info()
