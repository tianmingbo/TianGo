'''
https://qimingpian.cn/finosda/project/pquery
处理返回的数据加密
'''
import json

import requests
import execjs

node = execjs.get()

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "22",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "vipapi.qimingpian.cn",
    "Origin": "https://qimingpian.cn",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
}

payload = 'page=1&num=20&unionid='
url = 'https://vipapi.qimingpian.cn/search/productNewList'
res = requests.post(url, headers=headers, data=payload)
encrypt_data = json.loads(res.text)['encrypt_data']
with open('企名科技.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
real_data = ctx.eval(f'getData("{encrypt_data}")')
print(real_data)
