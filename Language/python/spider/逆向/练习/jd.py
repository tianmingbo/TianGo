"""
http://login.shikee.com/
根据form表单中value是不是password来判断，
另一个需要全局搜索rsa_n
"""
import execjs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer': 'https://passport.jd.com/uc/login?ltype=logout'
}
node = execjs.get()
with open('jd.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())

pwd = ctx.eval(f'getPwd("123456")')
print(pwd)
