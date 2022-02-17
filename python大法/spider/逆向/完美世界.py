import requests
from lxml import etree
import execjs

"""
公钥藏在页面中
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer': 'https://passport.wanmei.com/sso/login?service=passport&isiframe=1&location=2f736166652f'
}
url = 'https://passport.wanmei.com/sso/login?service=passport&isiframe=1&location=2f736166652f'
res = requests.get(url, headers=headers)
tree = etree.HTML(res.text)
key = tree.xpath("//input[@id='e']/@value")[0]

node = execjs.get()
with open('完美世界.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
print(f'getPwd(123456,{key})')
pwd = ctx.eval(f'getPwd("123456","{key}")')
print(pwd)
