"""
https://passport.kongzhong.com/
js混淆,需要进行js反混淆
反混淆方法：
1：线上反混淆工具（不理想）
2：浏览器自带的反混淆工具（推荐）**
   --设置->偏好设置->在匿名和内容脚本中搜索
   设置完毕之后，重新搜索，会出现一个VM开头的东西，就是反混淆的代码

密钥可能在某些请求中响应回来的，或者是在某个隐藏的元素里面
"""
import re
import requests
import execjs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer': 'https://passport.kongzhong.com/'
}
dc_url = 'https://sso.kongzhong.com/ajaxLogin?j=j&jsonp=j&service=https://passport.kongzhong.com/&_=1639213564622'
res = requests.get(dc_url, headers=headers)
dc_re = re.compile('"dc":"(.*?)","kzmsg"')
dc = re.findall(dc_re, res.text)[0]

node = execjs.get()
with open('空中网.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
pwd = ctx.eval(f'getPwd("123456","{dc}")')
print(pwd)
