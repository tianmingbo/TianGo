"""
http://login.shikee.com/
根据form表单中value是不是password来判断，
另一个需要全局搜索rsa_n
"""
import requests
import execjs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer': 'https://passport.wanmei.com/sso/login?service=passport&isiframe=1&location=2f736166652f'
}
url = 'http://login.shikee.com/getkey?v=c3c1dc9a7c3897c4658cee43816b2861'
res = requests.get(url).text
rsa = res.split('"')[-2]
print(rsa)
node = execjs.get()
with open('试客联盟.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())

pwd = ctx.eval(f'getPwd("{rsa}","{123456}")')
print(pwd)
