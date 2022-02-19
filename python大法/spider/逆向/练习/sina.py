import json
import re
import base64
import time
import requests
import execjs

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "login.sina.com.cn",
    "Referer": "http://my.sina.com.cn/",
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
}
node = execjs.get()
with open('sina.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
su = base64.b64encode('18848868890'.encode()).decode()


def pre_login():
    timestamp = int(time.time() * 1000)
    url = f'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.19)&_={timestamp}'
    res = requests.get(url, headers=headers)
    res = re.findall(re.compile('sinaSSOController.preloginCallBack\((.*)\)'), res.text)[0]
    res = json.loads(res)
    url = f"https://login.sina.com.cn/cgi/pin.php?r=66696755&s=0&p={res['pcid']}"
    with open("captcha.png", "wb") as f:
        f.write(requests.get(url).content)
    return res


def login(pre_info):
    timestamp = int(time.time() * 1000)
    pub_key = pre_info['pubkey']
    ser_time = pre_info['servertime']
    nonce = pre_info['nonce']
    pwd = 'woshihaoren666'
    sp = ctx.eval(f'getPwd("{pub_key}","{ser_time}","{nonce}","{pwd}")')
    url = f'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_={timestamp}'
    door = input('请输入验证码->')
    data = {
        "entry": "weibo",
        "gateway": "1",
        "from": "",
        "savestate": "7",
        "qrcode_flag": "true",
        "useticket": "1",
        "pagerefer": "https://weibo.com/newlogin?tabtype=weibo&gid=102803&url=https%3A%2F%2Fweibo.com%2F",
        "vsnf": "1",
        "door": door,
        "su": su,
        "service": "miniblog",
        "servertime": pre_info['servertime'],
        "nonce": pre_info['nonce'],
        "pwencode": "rsa2",
        "rsakv": pre_info['rsakv'],
        "sp": sp,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "2",
        "domain": "weibo.com",
        "prelt": "0",
        "returntype": "TEXT"
    }
    print(data)
    res = requests.post(url, headers=headers, data=data)
    print(res.text)
    print(res.cookies)


if __name__ == '__main__':
    pre_info = pre_login()
    # print(pre_info)
    login(pre_info)
