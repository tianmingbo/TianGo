"""
https://unicom_trip.133.cn/city/?system=cjfcts
难点：返回数据加密
"""
import json

import requests
import execjs

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "Referer": "https://unicom_trip.133.cn/city/?system=cjfcts"
}
url = 'https://unicom_trip.133.cn/city/?system=cjfcts'
csrf = cookie = ""
node = execjs.get()


def get_xsrf():
    res = requests.get(url, headers=headers)
    global csrf, cookie
    for k, v in res.cookies.items():
        if k == 'XSRF-TOKEN':
            csrf = v
        cookie += f'{k}={v};'
    if 'XSRF-TOKEN' in res.cookies.items():
        csrf = res.cookies['XSRF-TOKEN']


def get_data():
    data_url = 'https://unicom_trip.133.cn/api/v1/city/flight-route/SHA?date=20211218&type=arr'
    headers['cookie'] = cookie
    headers['X-XSRF-TOKEN'] = csrf
    res = requests.get(data_url, headers=headers)
    with open('人口流动态势大数据.js', 'r', encoding='utf-8') as f:
        ctx = node.compile(f.read())
    res = ctx.eval(f'dataDecode("{res.text}")')
    with open('map_info.json', 'r', encoding='utf-8') as f:
        map_info = json.loads(f.read())  # 地名map
    for i in res['data']:
        print(i)
        print(f'from {map_info["data"]["flight"].get(i["dep_city_code"], {}).get("city_name", i["dep_city_code"])} '
              f'to {map_info["data"]["flight"].get(i["arr_city_code"], {}).get("city_name", i["arr_city_code"])}')


if __name__ == '__main__':
    get_xsrf()
    get_data()
