import requests
import json
import time
import cv2
import numpy as np
import base64
import random
import math
from des import encrypt, decrypt


class Sm(object):
    def __init__(self):
        self.info_url = "https://captcha.fengkongcloud.com/ca/v1/register?organization=RlokQwRlVjUrTUlkIqOg&appId=default&channel=DEFAULT&lang=zh-cn&model=slide&rversion=1.0.1&sdkver=1.0.0&data=%7B%7D&callback=sm_{}".format(
            str(int(time.time() * 1000)))
        self.sub_url = "https://captcha.fengkongcloud.com/ca/v1/fverify"
        self.headers = {
            "Referer": "https://www.fengkongcloud.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def get_cap_info(self):
        info = requests.get(self.info_url, headers=self.headers).text
        return json.loads(info[17:-1])

    def download_cap(self, img, fn):
        res = requests.get(img)
        with open(fn, "wb") as f:
            f.write(res.content)

    def get_space(self):
        img1 = cv2.imread("bg.png", 0)
        img2 = cv2.imread("m2.jpg", 0)
        res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        loc = np.where(res >= 0.6)
        for pt in zip(*loc[::-1]):
            p = pt
        try:
            cv2.imshow('Detected', img1[p[1]:, p[0]:])
            cv2.waitKey(3000)
        except Exception as e:
            print(e)
            return None
        return p[0] * (290 / 600)

    def get_track(self, space):
        x = [0, 0]
        y = [0, 0, 0]
        z = [0]
        # x
        count = np.linspace(-math.pi / 2, math.pi / 2, random.randrange(20, 30))
        # print(count)
        func = list(map(math.sin, count))
        nx = [i + 1 for i in func]
        add = random.randrange(10, 15)
        sadd = space + add
        x.extend(list(map(lambda x: x * (sadd / 2), nx)))
        # x.extend(np.linspace(sadd, space, 4 if add > 12 else 3))
        x.extend(np.linspace(sadd, space, 3 if add > 12 else 2))
        x = [math.floor(i) for i in x]
        # y
        for i in range(len(x) - 2):
            if y[-1] < 30:
                y.append(y[-1] + random.choice([0, 0, 1, 1, 2, 2, 1, 2, 0, 0, 3, 3]))
            else:
                y.append(y[-1] + random.choice([0, 0, -1, -1, -2, -2, -1, -2, 0, 0, -3, -3]))
        # z
        for i in range(len(x) - 1):
            z.append((z[-1] // 100 * 100) + 100 + random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]))
        return list(map(list, zip(x, y, z)))

    def act(self, k, tracks, space):
        # 生成轨迹等参数加密的 key
        key = "sshummei"
        text = base64.b64decode(k)
        new_key = decrypt(key, text)[:8]
        print("new_key:", new_key)
        # 将轨迹等参数加密
        p = {
            # 滑动距离 / 300
            "d": space / 300,
            # 轨迹
            "m": tracks,
            # 滑动用时
            "c": tracks[-1][-1] + random.randint(30, 80),
            # "c":1367,
            #
            "cs": 1,
            # 是否为 webdriver
            "wd": 0
        }
        encryptText = json.dumps(p).replace(" ", "")
        print(encryptText)
        at = encrypt(new_key, encryptText)
        return at.decode()

    def submit(self, data):
        res = requests.get(self.sub_url, headers=self.headers, params=data).text
        return res

    def run(self):
        data = {
            "organization": "d6tpAY1oV0Kv5jRSgxQr",
            "appId": "default",
            "channel": "DEFAULT",
            "lang": "zh-cn",
            "rversion": "1.0.4",
            "sdkver": "1.1.3",
            "callback": "sm_{}".format(int(time.time() * 1000)),
        }
        # 获得验证码接口信息
        info = self.get_cap_info()
        print(info)
        # rid
        data["rid"] = info["detail"]["rid"]
        bg_url = "https://castatic.fengkongcloud.com{}".format(info["detail"]["bg"])
        # 下载验证码背景图
        self.download_cap(bg_url, "bg.png")
        # 获取缺口距离
        space = self.get_space()
        # space = 139
        if space:
            print(int(space))
            # 伪造轨迹
            tracks = self.get_track(int(space))
            # tracks = [
            #     [0, 3, 0],[0, 3, 101],[71, -1, 202],[119, -3, 302],[136, -7, 402],[141, -9, 501],[141, -9, 601],[141, -9, 701],[141, -9, 801],[140, -9, 902],[140, -9, 1001],[139, -8, 1101],[139, -8, 1202],[139, -8, 1301]
            # ]
            print(tracks)
            act = self.act(info["detail"]["k"], tracks, int(space))
            # act
            data["act"] = act
            # 提交
            print(data)
            res = self.submit(data)
            # "riskLevel":"PASS" 为通过
            print(res)
        else:
            print("space识别错误,请重试")


if __name__ == '__main__':
    sm = Sm()
    sm.run()

# '0R200ardIuemJQO/gFkOrZymCKQR16I+9OvC+McooRD9larRAZgrRf/OVt+jGs6UZak0/XnC/GHhGRV54t5z+HZOGBRL6ZjZlrmpQTZCDt778W7HYFi+XdFYb4yUd1/csnyjLImdlXQ/dmMA37zZnyhfm/jIerJKx5/gr5NkXTS8Vwq/C9zVNruVyGkIkCW3nLCmuSD1EZIwzGsu6OI2o1FW89iC9QzL3FYMQAX3T7BrsqUEc9ji0L0FtGjwWOvY1esFiYSvJO2j7Iar/8x3JcQtofIV273jMMVAZJsB3NtnBZYSsmWt2YMkVHRntCCFyOZ2faZBqeiXh/BGSi3WERWRJGkVkfgqqIdfs/CC+WpJYUntdzrS8dymqNG+2yJwtPklc/5vaEcKAh5sfnnRdJ8zseiXW89UaLwmkelFsp0aEAXBjDL/s6tyIV1ajri9ZRDxrgia8UQ81Es7kUs1gjalYSX49NMq8jWhCrcJlvviMmY0dBKL/FvL4OWFvv29F60bbkvhlTs62DxD47z6UevJbHq5Pz/FcmmPhSL9qo5rN2eP0k4o52wR06OmmFrGTUhOTnjBB7Y='
# "0R200ardIucJpsvxkiELKAHT74pEoBl09ry8C2r0yUAwByStV0BLlu8mUmgc4nD9C29Y3r0McHQERUkW89E1vonLwh9H7I+7VBQIOhAD73iFREydB52VYGjizJqFQThKmpaF5IvyHp4/pM2LpkG+Y72powNpWXkSWCLH+4NsB4VRIFSFEeBjHpeANFUEpsrFzaHwajW0ds5ncZSthrSlwEgG8UB/dRtAoOunv6NEfTxGLyGszfP1QLyytBGQ8q1MAsyJF/j4moCRuu8CX63/exf6YFe4lGuZBp7Cwqugky4l9pbDJIBRmQ=="
# '0R200ardIucJpsvxkiELKAHT74pEoBl09ry8C2r0yUAwByStV0BLlu8mUmgc4nD9C29Y3r0McHQERUkW89E1vonLwh9H7I+7VBQIOhAD73iFREydB52VYGjizJqFQThKmpaF5IvyHp4/pM2LpkG+Y72powNpWXkSWCLH+4NsB4VRIFSFEeBjHpeANFUEpsrFzaHwajW0ds5ncZSthrSlwEgG8UB/dRtAoOunv6NEfTxGLyGszfP1QLyytBGQ8q1MAsyJF/j4moCRuu8CX63/exf6YFe4lGuZBp7Cwqugky4l9pbDJIBRmQ=='
# "{"d":0.4633333333333333,"m":[[0,3,0],[0,3,101],[71,-1,202],[119,-3,302],[136,-7,402],[141,-9,501],[141,-9,601],[141,-9,701],[141,-9,801],[140,-9,902],[140,-9,1001],[139,-8,1101],[139,-8,1202],[139,-8,1301]],"c":1367,"cs":1,"wd":0}"
# "{"d":0.4,"m":[[0,15,0],[0,0,100],[1,1,201],[3,1,300],[6,3,400],[10,3,503],[14,5,600],[19,8,700],[25,10,802],[31,11,900],[38,12,1000],[45,14,1101],[52,16,1203],[60,18,1300],[68,21,1400],[75,22,1500],[83,24,1603],[90,24,1703],[97,25,1800],[104,27,1901],[110,27,2000],[116,28,2100],[121,30,2200],[125,29,2300],[129,31,2400],[132,29,2500],[134,30,2600],[135,27,2700],[136,30,2800],[136,28,2900],[130,31,3000],[125,29,3100],[120,29,3200]],"c":3248,"cs":1,"wd":0}"
