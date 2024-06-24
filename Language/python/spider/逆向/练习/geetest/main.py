# encoding: utf-8
import json
import re
import time
import execjs
import hashlib
import requests

from restore import restore_picture
from recognition import SlideCrack
from slide_path import slide_track


def get_pic():
    """
    获取被打乱的背景和对比图
    """
    time_stamp = int(time.time() * 1000)
    params = (('t', f'{time_stamp}'),)
    """
    注册滑块请求，响应预览中返回的信息中重要的是 gt 和 challenge，gt 是固定值，不同网页对应不同的 gt 值，类似于特征码，
    challenge 的值每次刷新页面都会变化，gt 参数会通过 url string 的形式传递给 gettype.php
    """
    response = session.get('https://www.geetest.com/demo/gt/register-slide', headers=headers, params=params)
    challenge = response.json().get('challenge')
    gt = response.json().get('gt')
    time_ = int(time.time() * 1000)
    params = (('gt', f'{gt}'), ('callback', f'geetest_{time_}'))
    # 返回一些 js 文件及对应的版本号
    session.get('https://apiv6.geetest.com/gettype.php', headers=headers, params=params)
    timestamp = int(time.time() * 1000)
    params = (
        ('gt', f'{gt}'),  # register-slide 响应返回的 gt 值；
        ('challenge', f'{challenge}'),  # register-slide 响应返回的 challenge 值；
        ('lang', 'zh-cn'),
        ('pt', '0'),
        ('client_type', 'web'),
        ('w', ''),  # 对轨迹、滑动时间等进行加密后的参数，该网站第一个 w 值可置空；
        ('callback', f'geetest_{timestamp}'),
    )
    session.get('https://apiv6.geetest.com/get.php', headers=headers, params=params)
    timestamp = int(time.time() * 1000)
    params = (
        ('gt', f'{gt}'),
        ('challenge', f'{challenge}'),
        ('lang', 'zh-cn'),
        ('pt', '0'),
        ('client_type', 'web'),
        ('w', ''),
        ('callback', f'geetest_{timestamp}'),
    )
    # 点击按钮进行验证
    session.get('https://api.geetest.com/ajax.php', headers=headers, params=params)
    timestamp = int(time.time() * 1000)
    params = (
        ('is_next', 'true'),
        ('type', 'slide3'),
        ('gt', f'{gt}'),
        ('challenge', f'{challenge}'),
        ('lang', 'zh-cn'),
        ('https', 'true'),
        ('protocol', 'https://'),
        ('offline', 'false'),
        ('product', 'embed'),
        ('api_server', 'api.geetest.com'),
        ('isPC', 'true'),
        ('autoReset', 'true'),
        ('width', '100%'),
        ('callback', f'geetest_{timestamp}'),
    )
    response = session.get('https://api.geetest.com/get.php', headers=headers, params=params)
    resp = json.loads(re.findall('geetest_\d+\((.*?)\)', response.text)[0])
    bg = resp.get('bg')  # 被打乱的带缺口背景图，需要还原
    fullbg = resp.get('fullbg')  # 被打乱的完整背景图，需要还原
    challenge = resp.get('challenge')
    gt = resp.get('gt')
    s = resp.get('s')  # 关键参数，与后面 aa 参数的值有关
    c = resp.get('c')  # 关键参数，与后面 aa 参数的值有关，固定值
    bg_url = 'https://static.geetest.com/' + bg
    fullbg_url = 'https://static.geetest.com/' + fullbg
    bg_pic = session.get(bg_url).content
    with open('bg_pic_.jpg', 'wb') as w:
        w.write(bg_pic)
    full_pic = session.get(fullbg_url).content
    with open('full_pic_.jpg', 'wb') as w:
        w.write(full_pic)
    return challenge, gt, s, c


def recover_pic():
    restore_picture('bg_pic_.jpg', 'bg_pic')
    restore_picture('full_pic_.jpg', 'full_pic')


def get_distance():
    img1 = "bg_pic.jpg"  # 带缺口的背景图
    img2 = "full_pic.jpg"  # 不带缺口的背景图
    gt = SlideCrack(img1, img2)
    val = gt.run()
    return val


def encrypt_md5(data):
    data = data
    md5 = hashlib.md5()
    md5.update(data.encode('utf8'))
    encrypt_data = md5.hexdigest()
    return encrypt_data


def __get_track():
    distance = get_distance() - 5
    arr_track = slide_track.get(distance) or slide_track.get(distance - 1) or slide_track.get(
        distance + 1) or slide_track.get(distance + 2) or slide_track.get(distance - 2)

    detail_track = []
    for i in range(len(arr_track) - 1):
        detail_track.append([arr_track[i + 1][0] - arr_track[i][0], arr_track[i + 1][1] - arr_track[i][1],
                             arr_track[i + 1][2] - arr_track[i][2]])
    return arr_track, detail_track


def verify(arr_track, detail_track, gt, challenge, rp, c, s, t, n):
    with open('geetest.js') as r:
        js_str = r.read()
    w = execjs.compile(js_str).call('get_w', arr_track, detail_track, gt, challenge, rp, c, s, t, n)
    time_ = int(time.time() * 1000)
    params = {
        'gt': f'{gt}',
        'challenge': f'{challenge}',
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        'w': f'{w}',
        'callback': f'geetest_{time_}',
    }

    response = session.get('https://api.geetest.com/ajax.php', headers=headers, params=params)
    print(response.text)
    return response


def run():
    challenge, gt, s, c = get_pic()
    recover_pic()
    arr_track, detail_track = __get_track()
    t = arr_track[-1][0]
    n = arr_track[-1][2]
    rp = encrypt_md5(gt + challenge[:32] + str(n))
    time.sleep(1)
    return verify(arr_track, detail_track, gt, challenge, rp, c, s, t, n)


if __name__ == '__main__':
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://www.geetest.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    session = requests.session()
    counter = 0
    for i in range(100):
        res = run()
        if '"success": 1' in res.text:
            counter += 1
    print(counter)
