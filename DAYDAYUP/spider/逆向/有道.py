"""
有道查询
"""
import random
import time

import execjs
import requests

headers = {
    'Cookie': 'OUTFOX_SEARCH_USER_ID=-1322346001@10.169.0.102; JSESSIONID=aaaIYhr03Zwwu9QgB6T2x; OUTFOX_SEARCH_USER_ID_NCOO=611581907.1834145; UM_distinctid=17dae58cdaa223-0c896d3fca7af9-1f396452-13c680-17dae58cdabca3; ___rl__test__cookies=1639309812984',
    'Referer': 'http://fanyi.youdao.com/',
    'User-Agent': '5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
}

node = execjs.get()
with open("有道.js", "r", encoding="utf-8") as f:
    ctx = node.compile(f.read())
i = int(time.time() * 1000) + int(random.random() * 10)
trans_word = input()
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
    'bv': 'db3e6fc05e1796cb0030cda74ecb0567',  # md5(User-Agent)
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
}
print(data)
res = requests.post(trans_url, headers=headers, data=data).json()
print(res)
