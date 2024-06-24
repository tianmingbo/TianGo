#!/usr/bin/env python
# -*- coding:utf-8 -*-
from os.path import dirname, abspath
import os
from urllib.request import urlopen

import requests
import json
import time
import cv2
import numpy as np
import base64
import random
from des import encrypt, decrypt

headers = {
    "cookie": "cookie: smidV2=2020030823214532b9386755b96f8d9e2c2d61a27e3e4d00c8f0fe528ce4960; xhsTrackerId=3fc56aab-800d-48a3-c87f-46d939517c41; timestamp1=966284780; hasaki=JTVCJTIyTW96aWxsYSUyRjUuMCUyMChNYWNpbnRvc2glM0IlMjBJbnRlbCUyME1hYyUyME9TJTIwWCUyMDEwXzE1XzMpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGODAuMC4zOTg3LjEyMiUyMFNhZmFyaSUyRjUzNy4zNiUyMiUyQyUyMnpoLUNOJTIyJTJDMjQlMkMtNDgwJTJDdHJ1ZSUyQ3RydWUlMkN0cnVlJTJDJTIydW5kZWZpbmVkJTIyJTJDJTIyZnVuY3Rpb24lMjIlMkNudWxsJTJDJTIyTWFjSW50ZWwlMjIlMkMxMiUyQzglMkNudWxsJTJDJTIyQ2hyb21lJTIwUERGJTIwUGx1Z2luJTNBJTNBUG9ydGFibGUlMjBEb2N1bWVudCUyMEZvcm1hdCUzQSUzQWFwcGxpY2F0aW9uJTJGeC1nb29nbGUtY2hyb21lLXBkZn5wZGYlM0JDaHJvbWUlMjBQREYlMjBWaWV3ZXIlM0ElM0ElM0ElM0FhcHBsaWNhdGlvbiUyRnBkZn5wZGYlM0JOYXRpdmUlMjBDbGllbnQlM0ElM0ElM0ElM0FhcHBsaWNhdGlvbiUyRngtbmFjbH4lMkNhcHBsaWNhdGlvbiUyRngtcG5hY2x+JTIyJTJDMzgwMTgwMDQ1NyU1RA==; timestamp2=3b60c3fd464c80752d2aba3b549018a3; xhs_spid.5dde=6ec9d1ca3a610f2a.1583680905.2.1583719909.1583682674.8e0ddb5a-05ef-413b-9b15-b6c2c2df924d",
    "Referer": "https://www.xiaohongshu.com/web-login/captcha?redirectPath=http%3A%2F%2Fwww.xiaohongshu.com%2Fuser%2Fprofile%2F5885bc185e87e771bd4647e7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}


def _init_slider():
    """
    初始化验证码
    :return:
    """
    url = 'https://captcha.fengkongcloud.com/ca/v1/register'
    params = {
        'organization': 'eR46sBuqF0fdw7KWFLYa',
        'appId': 'default',
        'channel': 'web',
        'lang': 'zh-cn',
        'model': 'slide',
        'rversion': '1.0.1',
        'sdkver': '1.1.3',
        'data': {},
        'callback': 'sm_{}'.format(int(time.time() * 1000))
    }
    resp = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=5)
    result = json.loads(resp.text.replace('{}('.format(params['callback']), '').replace(')', ''))
    print(result)
    if result['riskLevel'] == 'PASS':
        return {
            'k': result['detail']['k'],
            'captcha_url': 'https://castatic.fengkongcloud.com{}'.format(result['detail']['bg']),
            'slider_url': 'https://castatic.fengkongcloud.com{}'.format(result['detail']['fg']),
            'rid': result['detail']['rid']
        }
    return None


def _encrypt_trace(k, trace, distance):
    """
    加密轨迹
    :param k: 初始密钥
    :param trace: 轨迹
    :param distance: 距离
    :return:
    """
    # 对 k 值进行 base64 解码
    text = base64.b64decode(k)
    # 对解码后的 k 值进行 DES 解密（密钥: sshummei）, 取前8位作为下一次加密的密钥
    new_key = decrypt('￥', text)[:8]
    # 构造待加密数据
    data = {
        # 滑动距离 / 300
        "d": distance / 300,
        # 轨迹
        "m": trace,
        # 滑动所用时间
        "c": trace[-1][-1],
        # 验证码图片尺寸, 宽
        "w": 300,
        # 验证码图片尺寸, 高
        'h': 150,
        # 设备
        'os': 'web_pc',
        # 是否 webdriver
        "cs": 0,
        "wd": 0,
        'sm': -1
    }
    # 最后加密 DES
    return encrypt(new_key, json.dumps(data).replace(' ', '')).decode()


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    img_path = os.path.abspath(os.path.dirname(__file__)) + '/' + '{}.jpg'.format(type)
    img_data = requests.get(url, proxies=proxies, timeout=5).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def _get_distance(fg, bg, resize_num=1):
    """
    找出图像中最佳匹配位置
    :param target_src: 目标即背景图
    :param template_src: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    fg_obj = download_imdecode(src=fg)
    fg_gray = cv2.cvtColor(fg_obj, cv2.COLOR_BGR2GRAY)
    bg_obj = download_imdecode(bg, flag=0)
    
    res = cv2.matchTemplate(fg_gray, bg_obj, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(res)
    distance = max_indx[0] * resize_num
    return distance


def download_imdecode(src, flag=3):
    """下载图片到内存, 生成image对象"""
    resp = urlopen(src)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, flag)
    return image


def _get_distance_old(slider_url, captcha_url):
    """
    获取缺口距离
    :param captcha_url: 验证码 url
    :return:
    """
    slider_img_path = _pic_download(slider_url, 'slider')
    bg_img_path = _pic_download(captcha_url, 'captcha')
    img1 = cv2.imread(bg_img_path, 0)
    img2 = cv2.imread(slider_img_path, 0)
    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.6)
    for pt in zip(*loc[::-1]):
        p = pt
    # try:
    #     cv2.imshow('Detected', img1[p[1]:, p[0]:])
    #     cv2.waitKey(3000)
    # except Exception as e:
    #     print(e.args)
    #     return None
    # res = cv2.resize(img1, (255, int(300 * (255 / 600))), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("res", res[:, int(p[0] * (255 / 600) + 15):])
    # cv2.waitKey(3000)
    return int(p[0] * (290 / 600))


def _generate_trace(distance, start_time):
    """
    生成轨迹
    :param distance:
    :param start_time:
    :return:
    """
    back = random.randint(2, 6)
    distance += back
    # 初速度
    v = 0
    # 位移/轨迹列表，列表内的一个元素代表0.02s的位移
    tracks_list = []
    # 当前的位移
    current = 0
    while current < distance - 13:
        # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
        a = random.randint(10000, 12000)  # 加速运动
        # 初速度
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        # 当前的位置
        current += s
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t / 1000
        # 添加到轨迹列表
        if current < distance:
            tracks_list.append(round(current))
    # 减速慢慢滑
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    # 回退
    for _ in range(back):
        current -= 1
        tracks_list.append(round(current))
    tracks_list.append(round(current) - 1)
    if tracks_list[-1] != distance - back:
        tracks_list.append(distance - back)
    # 生成时间戳列表
    timestamp_list = []
    timestamp = int(time.time() * 1000)
    for i in range(len(tracks_list)):
        t = random.randint(11, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    zy = 0
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
             0, -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, -1, 0, 0])
        zy += y
        y_list.append(zy)
        j += 1
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append([x, y_list[index], timestamp_list[index] - start_time])
    return trace


def _slider_verify(act, rid):
    """
    验证
    :param act:
    :param rid:
    :return:
    """
    url = 'https://captcha.fengkongcloud.com/ca/v1/fverify'
    params = {
        "organization": "eR46sBuqF0fdw7KWFLYa",
        "appId": "default",
        "channel": "DEFAULT",
        "act": act,
        "rid": rid,
        "lang": "zh-cn",
        "ostype": "web",
        "rversion": "1.0.1",
        "sdkver": "1.1.3",
        "callback": "sm_{}".format(int(time.time() * 1000)),
    }
    resp = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=5)
    print(resp.headers)
    print(resp.url)
    result = json.loads(resp.text.replace('{}('.format(params['callback']), '').replace(')', ''))
    print(result)
    return result


def download_cap(img, fn):
    res = requests.get(img)
    with open(fn, "wb") as f:
        f.write(res.content)


def crack():
    """
    滑块验证
    :return:
    """
    while True:
        _init_data = _init_slider()
        if _init_data:
            break
        time.sleep(random.random())
    print('滑块初始化成功! ')
    fg_url = _init_data['slider_url']
    bg_url = _init_data['captcha_url']
    download_cap(fg_url, 'fg.png')
    download_cap(bg_url, 'bg.png')
    
    distance = _get_distance(fg=_init_data['slider_url'], bg=_init_data['captcha_url'])
    distance = int(distance / 2)
    # distance = _get_distance_old(_init_data['slider_url'], _init_data['captcha_url'])
    # if distance:
    #     print("新函数的距离", distance_new)
    #     print("旧的函数距离", distance)
    if not distance:
        return {
            'success': 0,
            'message': '缺口距离获取失败! ',
            'data': None
        }
    start_time = int(time.time() * 1000)
    time.sleep(random.uniform(0.01, 0.05))
    trace = _generate_trace(distance, start_time)
    act = _encrypt_trace(_init_data['k'], trace, distance)
    rid = _init_data['rid']
    result = _slider_verify(act, rid)
    if result['riskLevel'] == 'PASS':
        return {
            'success': 1,
            'message': '校验成功! ',
            'data': rid
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def xhs_capture_verify(rid):
    import requests
    
    cookies = {
        'smidV2': '2020030823214532b9386755b96f8d9e2c2d61a27e3e4d00c8f0fe528ce4960',
        'xhsTrackerId': '296b8562-b1d4-425c-c257-fc0c26ec4c0b',
        'timestamp1': '170352493',
        'hasaki': 'JTVCJTIyTW96aWxsYSUyRjUuMCUyMChNYWNpbnRvc2glM0IlMjBJbnRlbCUyME1hYyUyME9TJTIwWCUyMDEwXzE1XzMpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGODAuMC4zOTg3LjEzMiUyMFNhZmFyaSUyRjUzNy4zNiUyMiUyQyUyMnpoLUNOJTIyJTJDMjQlMkMtNDgwJTJDdHJ1ZSUyQ3RydWUlMkN0cnVlJTJDJTIydW5kZWZpbmVkJTIyJTJDJTIyZnVuY3Rpb24lMjIlMkNudWxsJTJDJTIyTWFjSW50ZWwlMjIlMkMxMiUyQzglMkNudWxsJTJDJTIyQ2hyb21lJTIwUERGJTIwUGx1Z2luJTNBJTNBUG9ydGFibGUlMjBEb2N1bWVudCUyMEZvcm1hdCUzQSUzQWFwcGxpY2F0aW9uJTJGeC1nb29nbGUtY2hyb21lLXBkZn5wZGYlM0JDaHJvbWUlMjBQREYlMjBWaWV3ZXIlM0ElM0ElM0ElM0FhcHBsaWNhdGlvbiUyRnBkZn5wZGYlM0JOYXRpdmUlMjBDbGllbnQlM0ElM0ElM0ElM0FhcHBsaWNhdGlvbiUyRngtbmFjbH4lMkNhcHBsaWNhdGlvbiUyRngtcG5hY2x+JTIyJTJDMzgwMTgwMDQ1NyU1RA==',
        'timestamp2': 'b049c72136b968427e091f3f2a983821',
        'xhs_spses.5dde': '*',
        'xhs_spid.5dde': 'e79a8d3e9aa79b81.1583730809.11.1583898988.1583893956.4a1fec74-76bf-4758-934d-b07b9ab3baa1',
    }
    
    headers = {
        'Host': 'www.xiaohongshu.com',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Dest': 'empty',
        'X-Sign': 'X586039fbdde8a4a35274f35c5c39ba72',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.xiaohongshu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.xiaohongshu.com/web-login/captcha?redirectPath=http%3A%2F%2Fwww.xiaohongshu.com%2Fuser%2Fprofile%2F595657e450c4b408a2cb9581',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    data = '{"rid":"'+rid+'","callFrom":"web","deviceId":"WHJMrwNw1k/Hy/Tx+X/36g2k+xaNjmJ+v0OrED2kbkCE/eiCwSUJYswisypSvYrtg5b9ZwGK+MxslpyQ8tA/IHBX8kjZlkN3dyeDVhN8AJwtXbErcf8zlJt0zlieX3yDdb2GXgZ5AQVJ276inF+53rrf1T5xekz1fJB82l5Rly3wFSN3V/llXmZImwuKz3oVCEU5AHex/3lo1z/xKzj/bf73AMzP0mKSPLBXJ4dNvFWNhTtnuuR8r/z4kGeHoWDZp1487582755342","status":1}'
    print(data)
    response = requests.post('https://www.xiaohongshu.com/fe_api/burdock/v2/shield/captcha', headers=headers,
                             cookies=cookies, data=data, proxies=proxies, timeout=5)
    print(response.text)


def shumei_verify():
    import requests
    
    headers = {
        'Host': 'fp-it.fengkongcloud.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'sec-fetch-dest': 'script',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'referer': 'https://www.xiaohongshu.com/web-login/captcha?redirectPath=http%3A%2F%2Fwww.xiaohongshu.com%2Fuser%2Fprofile%2F595657e450c4b408a2cb9581',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    timestamp = str(int(time.time())*1000)
    params = (
        ('callback', 'smCB_{}'.format(timestamp)),
        ('organization', 'eR46sBuqF0fdw7KWFLYa'),
        ('smdata',
         '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1487577677129'),
        ('os', 'web'),
        ('version', '2.0.0'),
        ('_', timestamp),
    )
    
    response = requests.get('https://fp-it.fengkongcloud.com/v3/profile/web', headers=headers, params=params)
    print('='*30)
    print(response.text)


def verify():
    x = crack()
    if x['success']:
        rid = x['data']
        xhs_capture_verify(rid=rid)
        shumei_verify()


if __name__ == '__main__':
    abu_proxy = "http://H543N64CA5P7XQ8D:49A4252F17153F70@http-dyn.abuyun.com:9020"
    proxies = {'http': abu_proxy, 'https': abu_proxy}
    proxies = {}
    headers = {
        'authority': 'www.xiaohongshu.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'referer': 'https://www.xiaohongshu.com/discovery/item/5e658dd10000000001001a9d',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'smidV2=2020030823214532b9386755b96f8d9e2c2d61a27e3e4d00c8f0fe528ce4960; xhsTrackerId=296b8562-b1d4-425c-c257-fc0c26ec4c0b; timestamp1=170352493; hasaki=JTVCJTIyTW96aWxsYSUyRjUuMCUyMChNYWNpbnRvc2glM0IlMjBJbnRlbCUyME1hYyUyME9TJTIwWCUyMDEwXzE1XzMpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGODAuMC4zOTg3LjEzMiUyMFNhZmFyaSUyRjUzNy4zNiUyMiUyQyUyMnpoLUNOJTIyJTJDMjQlMkMtNDgwJTJDdHJ1ZSUyQ3RydWUlMkN0cnVlJTJDJTIydW5kZWZpbmVkJTIyJTJDJTIyZnVuY3Rpb24lMjIlMkNudWxsJTJDJTIyTWFjSW50ZWwlMjIlMkMxMiUyQzglMkNudWxsJTJDJTIyQ2hyb21lJTIwUERGJTIwUGx1Z2luJTNBJTNBUG9ydGFibGUlMjBEb2N1bWVudCUyMEZvcm1hdCUzQSUzQWFwcGxpY2F0aW9uJTJGeC1nb29nbGUtY2hyb21lLXBkZn5wZGYlM0JDaHJvbWUlMjBQREYlMjBWaWV3ZXIlM0ElM0ElM0ElM0FhcHBsaWNhdGlvbiUyRnBkZn5wZGYlM0JOYXRpdmUlMjBDbGllbnQlM0ElM0ElM0ElM0FhcHBsaWNhdGlvbiUyRngtbmFjbH4lMkNhcHBsaWNhdGlvbiUyRngtcG5hY2x+JTIyJTJDMzgwMTgwMDQ1NyU1RA==; timestamp2=b049c72136b968427e091f3f2a983821; extra_exp_ids=; xhs_spses.5dde=*; xhs_spid.5dde=e79a8d3e9aa79b81.1583730809.5.1583819850.1583817807.a385e297-6dc1-489d-8de6-272d49ed411e',
    }
    response = requests.get('https://www.xiaohongshu.com/user/profile/5c3b5f3a000000000601b731', proxies=proxies, timeout=5, headers=headers)
    if "滑块验证" in response.text:
        users = ['SCU69239Tabd069307ab2a0d57fe3942d1e1007845df88c9327087']
        for user in users:
            send_url = f'https://sc.ftqq.com/{user}.send?text=fuck，小红书解封程序挂掉了...，请检查'
            requests.get(send_url)
        print("被封禁")
        verify()
    else:
        time.sleep(10)
        print('未封禁')