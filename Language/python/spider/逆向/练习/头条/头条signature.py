"""
jsvmp
jsdom补环境
"""
import execjs
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}

url = "https://www.toutiao.com/search/suggest/hot_words/"

with open('tmp2.js', 'r', encoding='utf-8') as f:
    js = f.read()
    _signature = execjs.compile(js).call('getSignature')

params = {
    "_signature": _signature
}

response = requests.get(url, params=params, verify=False)
print(response.text)
