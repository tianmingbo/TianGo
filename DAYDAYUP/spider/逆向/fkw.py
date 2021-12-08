import execjs

# js闭包直接可用,不用调试

node = execjs.get()
with open('fkw.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
pwd = ctx.eval('md5("123456")')
print(pwd)
