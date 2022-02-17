# 微信公众平台
# 安装PyExecJs来执行js代码
# 通过 发条js调试工具 调试代码

import execjs

node = execjs.get()
with open('wechat.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
pwd = ctx.eval('getPwd("123456")')
print(pwd)
