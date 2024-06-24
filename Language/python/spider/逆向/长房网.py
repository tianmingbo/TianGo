"""
http://eip.chanfine.com/login.jsp
主要难点在于需要根据sessionid来生成key，iv。
security是固定的参数
"""

import execjs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer': 'http://eip.chanfine.com/login.jsp?login_error=1'
}

node = execjs.get()
with open('长房网.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())

pwd = ctx.eval(f'getPwd("123456")')
print(pwd)
