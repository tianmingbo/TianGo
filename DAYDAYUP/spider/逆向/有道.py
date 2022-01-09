"""
有道查询
"""
import random
import time

import execjs
import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "237",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "OUTFOX_SEARCH_USER_ID=747953828@10.169.0.81; JSESSIONID=aaacpwKf3-wdW4yixg_4x; OUTFOX_SEARCH_USER_ID_NCOO=1451782132.6604552; ___rl__test__cookies=1641720473883",
    "Host": "fanyi.youdao.com",
    "Origin": "https://fanyi.youdao.com",
    "Referer": "https://fanyi.youdao.com/",
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

node = execjs.get()
with open("有道.js", "r", encoding="utf-8") as f:
    ctx = node.compile(f.read())
i = int(time.time() * 1000) + int(random.random() * 10)
trans_word = input('word:')
sign = ctx.eval(f'getSign("{trans_word}","{i}")')
trans_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
salt = str(int(time.time() * 10000))
data = {
    'i': trans_word,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'lts': salt[:-1],
    'bv': '8d23065ed7a771e2e350e99cab9568b8',  # md5(User-Agent)
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
}
print(data)
res = requests.post(trans_url, headers=headers, data=data).json()
print(res)
