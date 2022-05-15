# @Time : 2022/5/7 11:46
# @Author :bo~
# @FileName: tmp.py
# @Description:

# -*- coding:utf-8 -*-
import json
import logging
import os
import random
import re
import time
import urllib
import execjs
import requests
import sys
import urllib3
import tempfile
from PIL import Image
from requests.packages.urllib3 import disable_warnings
from const import *

disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
js_path = os.path.join(os.path.dirname(__file__), 'js')


class Decrypt:
    def __init__(self, js_path=''):
        js_path = js_path if js_path else os.path.join(js_path, 'js2.js')
        self.js = self.__read_js(js_path)

    # 读取js
    def __read_js(self, js_path):
        '''
        :param js_path: js路径
        :return:
        '''
        htmlstr = ''
        with open(js_path, 'r', encoding='utf-8') as f:
            htmlstr = f.read()
        return htmlstr

    def decrypt_pwd(self, pwd, qq, verifycode):
        '''
        加密QQ密码
        :param js_path: js路径
        :param pwd: 明文密码
        :param qq: qq号
        :param verifycode: 4位验证码
        :return: 加密后密码
        '''
        ctx = execjs.compile(self.js)
        return ctx.call('getPwd', pwd, qq, verifycode)

    def decrypt_cdata(self, et):
        ctx = execjs.compile(self.js)
        return ctx.call('getcdata', et)

    def decrypt_badbdd(self, mouse):
        ctx = execjs.compile(self.js)
        return ctx.call('getbadbdd', mouse)

    def decrypt_ua(self, ua):
        ctx = execjs.compile(self.js)
        return ctx.call('Bt', ua)

    def decrypt_tokenid(self):
        ctx = execjs.compile(self.js)
        return ctx.call('gettokenid')

    def decrypt_callback(self):
        ctx = execjs.compile(self.js)
        return ctx.call('callback')


class Verify:
    check_url = 'https://ssl.ptlogin2.qq.com/check'

    def __init__(self, parent):
        self.parent = parent

    def check(self):
        params = {
            'regmaster': '',
            'pt_tea': '2',
            'pt_vcode': '1',
            'uin': self.parent.qq,  # qq号
            'appid': self.parent.param['param']['appid'],
            'js_ver': '22042810',
            'js_type': '1',
            'login_sig': self.parent.cookies['pt_login_sig'],
            'u1': 'https://graph.qq.com/oauth2.0/login_jump',
            'r': '0.3558524842790869',
            'pt_uistyle': '40',
            'daid': self.parent.param['param']['daid'],
            'pt_3rd_aid': self.parent.param['param']['pt_3rd_aid'],
            'o1vId': 'c49b27c5674cf61587a47928903f7219'
        }
        g = self.parent.fetch(self.check_url, params=params, headers=headers2).text
        v = re.findall('\'(.*?)\'', g)
        self.pt_vcode_v1, self.vcode, self.uin, self.ptvfsession, _, _, self.sid = v
        if self.pt_vcode_v1 == '1':
            logger.info('QQ:%s 检测需要验证码' % self.parent.qq)
        return v

    def verify_islogin(self, response):
        gg = re.findall('\'(.*?)\'', response)
        if gg[0] == '0':
            qq_login_res = {'error': int(gg[0]), 'info': gg[-2], 'nickname': gg[-1], 'jump_url': gg[2]}
        else:
            qq_login_res = {'error': int(gg[0]), 'info': gg[4]}
        return qq_login_res

    def checkCaptch(self, info):
        if info['errorCode'] == "0":
            logger.info('成功识别滑块，^ v ^' + str(info))
            self.vcode = info['randstr']
            self.ptvfsession = info['ticket']
            return True
        else:
            logger.error('识别滑块失败，^ ^!')
            return False


class Captch:
    captch_url_1 = 'https://t.captcha.qq.com/cap_union_prehandle'
    vsig_url = 'https://t.captcha.qq.com/cap_union_new_show'
    post_url = 'https://ssl.captcha.qq.com/cap_union_new_verify?random=%d' % int(time.time())

    def __init__(self, parent):
        self.parent = parent
        self.param = self.fetch_params

    @property
    def fetch_params(self):
        # params = {
        #     'aid': self.parent.param['param']['appid'],
        #     'asig': '',
        #     'captype': '',
        #     'protocol': 'https',
        #     'clientype': '2',
        #     'disturblevel': '',
        #     'apptype': '2',
        #     'curenv': 'inner',
        #     'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjQ4NDMuNDAwIFFRQnJvd3Nlci85LjcuMTMwMjEuNDAw',
        #     'uid': self.parent.qq,
        #     'cap_cd': self.parent.verifier.vcode,
        #     'lang': '2052',
        #     'callback': Decrypt(os.path.join(js_path, 'tokenid.js')).decrypt_callback(),
        # }
        params = {
            "aid": self.parent.param['param']['appid'],
            "protocol": "https", "accver": "1", "showtype": "embed",
            "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMS4wLjQ5NTEuNTQgU2FmYXJpLzUzNy4zNiBFZGcvMTAxLjAuMTIxMC4zOQ==",
            "noheader": "1", "fb": "1", "aged": "0", "enableAged": "0", "enableDarkMode": "0",
            "sid": self.parent.verifier.sid,
            "grayscale": "1", "clientype": "2", "cap_cd": "", "uid": "", "wxLang": "", "lang": "zh-CN",
            "entry_url": "https://graph.qq.com/oauth2.0/login_jump",
            "elder_captcha": "0", "js": "/tcaptcha-frame.04b101bd.js",
            "login_appid": "", "wb": "2", "subsid": "1",
            "callback": Decrypt(os.path.join(js_path, 'tokenid.js')).decrypt_callback(),
            "sess": ""
        }
        r = self.parent.fetch(self.captch_url_1, headers=captcha_headers, params=params)
        return json.loads(re.findall('\((.*?)\)', r.text)[0])

    def fetch_vsig(self):
        # params = {
        #     'aid': self.parent.param['param']['appid'],
        #     'asig': '',
        #     'captype': '',
        #     'protocol': 'https',
        #     'clientype': '2',
        #     'disturblevel': '',
        #     'apptype': '2',
        #     'curenv': 'inner',
        #     'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjQ4NDMuNDAwIFFRQnJvd3Nlci85LjcuMTMwMjEuNDAw',
        #     'sess': self.param['sess'],
        #     'theme': '',
        #     'sid': self.param['sid'],
        #     'noBorder': 'noborder',
        #     'fb': '1',
        #     'forcestyle': 'undefined',
        #     'showtype': 'embed',
        #     'uid': self.parent.qq,
        #     'cap_cd': self.parent.verifier.vcode,
        #     'lang': '2052',
        #     'rnd': '81588',
        # }
        params = {
            "aid": self.parent.param['param']['appid'],
            "protocol": "https", "accver": "1", "showtype": "embed",
            "ua": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMS4wLjQ5NTEuNTQgU2FmYXJpLzUzNy4zNiBFZGcvMTAxLjAuMTIxMC4zOQ==",
            "noheader": "1", "fb": "1", "aged": "0", "enableAged": "0", "enableDarkMode": "0",
            "sid": self.param['sid'],
            "grayscale": "1", "clientype": "2",
            'sess': self.param['sess'],
            "fwidth": "0", "wxLang": "", "tcScale": "1", "uid": "", "cap_cd": "", "rnd": "295920",
            "prehandleLoadTime": "1148",
            "createIframeStart": int(time.time() * 1000),
            "global": "0", "subsid": "2"
        }
        r = self.parent.fetch(self.vsig_url, headers=captcha_headers, params=params)
        self.image_id = re.findall('cdnPic1:"/hycdn\?index=1&image=(.*?)",', r.text)[0]
        self.sess = re.findall('sess:"(.*?)",', r.text)[0]
        # self.vsig = re.findall('Q="(.*?)",', r.text)[0]
        # self.capthc_url = re.findall('ct="(.*?)",', r.text)[0]
        # self.websig = re.findall('websig:"(.*?)",', r.text)[0]
        # self.et = re.findall('et="(.*?)",', r.text)[0]
        # self.y = re.findall('Number\("(.*?)"\)', r.text)[0]

    def fetch_captch(self):
        # 获取滑动验证码图片
        self.fetch_vsig()
        # params = {
        #     'aid': self.parent.param['param']['appid'],
        #     'asig': '',
        #     'captype': '',
        #     'protocol': 'https',
        #     'clientype': '2',
        #     'disturblevel': '',
        #     'apptype': '2',
        #     'curenv': 'inner',
        #     'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjQ4NDMuNDAwIFFRQnJvd3Nlci85LjcuMTMwMjEuNDAw',
        #     'sess': self.param['sess'],
        #     'theme': '',
        #     'sid': self.param['sid'],
        #     'noBorder': 'noborder',
        #     'fb': '1',
        #     'forcestyle': 'undefined',
        #     'showtype': 'embed',
        #     'uid': self.parent.qq,
        #     'cap_cd': self.parent.verifier.vcode,
        #     'lang': '2052',
        #     'rnd': '510878',
        #     'rand': '0.1912210979675959',
        #     'vsig': self.vsig,
        #     'img_index': '1',
        # }
        params = {
            "index": "1",
            "image": f"{self.image_id}?aid={self.parent.param['param']['appid']}",
            "sess": self.sess,
            "sid": self.param['sid'],
            "img_index": "1", "subsid": "3"
        }
        captcha_url = 'https://t.captcha.qq.com/hycdn'
        r = self.parent.fetch(captcha_url, headers=captcha_headers, params=params)
        img_path = os.path.join(os.getcwd(), 'captch.png')
        with open(img_path, 'wb') as f:
            f.write(r.content)
        return self.post_captch(self.gen_guiji(self.fetch_distance(img_path)))

    def gen_guiji(self, x):
        print(x)
        tkid = Decrypt(os.path.join(js_path, 'tokenid.js')).decrypt_tokenid()
        self.cdata = Decrypt(os.path.join(js_path, 'getcdata.js')).decrypt_cdata(self.et)
        self.x = x
        x = int(x // 2.428)

        slideValue = []
        mouseDownValue = [{
            "t": random.randint(100, 120),
            "x": random.randint(55, 65),
            # "y": random.randint(200, 287),
            "y": random.randint(188, 220),
        }]

        slideValue.append([mouseDownValue[0]['x'], mouseDownValue[0]['y'], mouseDownValue[0]['t']])
        r = mouseDownValue[0]['x']
        while r < x - mouseDownValue[0]['x']:
            if x - r <= 36:
                slideValue.append([random.randint(1, 2), random.randint(0, 1), random.randint(17, 45)])
            else:
                slideValue.append([random.randint(1, 6), random.randint(-2, 2), random.randint(7, 16)])
            r += slideValue[-1][0]
        slideValue.append([0, 0, int(self.cdata)])
        s_x = 0
        s_y = 0
        s_t = 0
        for i in slideValue:
            s_x += i[0]
            s_y += i[1]
            s_t += i[2]

        mouseUpValue = [{
            "t": random.randint(170, 200),
            "x": s_x,
            "y": s_y,
        }]

        # print(x, s_x, s_y, s_t)

        begintime = int(time.time()) - (s_t // 1000)
        endtime = int(time.time())
        # time.sleep(s_t // 1000)
        logger.info('模拟滑块轨迹为：' + str(slideValue))
        guiji = {"mouseclick": mouseDownValue,
                 "keyvalue": [],
                 "user_Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 QQBrowser/9.7.13021.400",
                 "resolutionx": 1366, "resolutiony": 768, "winSize": [300, 230],
                 "url": "https://ssl.captcha.qq.com/cap_union_new_show",
                 "refer": "https://xui.ptlogin2.qq.com/cgi-bin/xlogin", "begintime": begintime,
                 "endtime": endtime,
                 "platform": 1,
                 "os": 'other', "keyboards": 0, "flash": 1, "pluginNum": 10, "index": 5, "ptcz": "",
                 "tokenid": tkid,
                 "a": tkid, "btokenid": 'null', "tokents": begintime, "ips": {"in": ["192.168.4.158"]},
                 "colorDepth": 24,
                 "cookieEnabled": 'true', "timezone": 8, "wDelta": 0,
                 "mousemove": slideValue, "keyUpCnt": 0,
                 "keyUpValue": [],
                 "mouseUpValue": mouseUpValue, "mouseUpCnt": 1, "mouseDownValue": mouseDownValue,
                 "mouseDownCnt": 1,
                 "orientation": [{"x": 0, "y": 0, "z": 0}], "bSimutor": 0, "focusBlur": {"in": [], "out": [], "t": []},
                 "fVersion": 26.9, "charSet": "UTF-8", "resizeCnt": 0, "errors": [],
                 "screenInfo": "1366-768-728-24-*-*-*",
                 "elapsed": 7000, "ft": "qf_7P_n_H", "coordinate": [10, 24, 0.40512820512820513], "clientType": "2",
                 "trycnt": 5,
                 "refreshcnt": 0,
                 "slideValue": slideValue, "dragobj": 0}
        return json.dumps(guiji)

    def judge_islike(self, im, x, y):
        pix0 = im.getpixel((x, y))
        pix1 = im.getpixel((x + 1, y + 1))
        s_pix = 0
        for i in range(0, 3):
            s_pix += abs(pix1[i] - pix0[i])
        return s_pix // 3

    def fetch_distance(self, img_path):
        im = Image.open(img_path)
        width, height = im.size
        x1, x2, times = 0, 0, 0
        for y in range(height - 1):
            flag = False
            for x in range(width - 1):
                if self.judge_islike(im, x, y) > 20:
                    x1, x2 = x + 1, x1
                    if 100 < abs(x2 - x1) < 105:
                        times += 1
                        flag = True if times > 5 else False
            if flag:
                break
        logger.info('左边到滑块右边距离为：%d' % x2)
        return x2 - 89

    def post_captch(self, mouse):
        data = {
            'aid': self.parent.param['param']['appid'],
            'asig': '',
            'captype': '',
            'protocol': 'https',
            'clientype': '2',
            'disturblevel': '',
            'apptype': '2',
            'curenv': 'inner',
            'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjQ4NDMuNDAwIFFRQnJvd3Nlci85LjcuMTMwMjEuNDAw',
            'sess': self.param['sess'],
            'theme': '',
            'sid': self.param['sid'],
            'noBorder': 'noborder',
            'fb': '1',
            'forcestyle': 'undefined',
            'showtype': 'embed',
            'uid': self.parent.qq,
            'cap_cd': self.parent.verifier.vcode,
            'lang': '2052',
            'rnd': random.randint(579754, 777777),
            'subcapclass': '13',
            'vsig': self.vsig,
            'ans': '%d,%s;' % (self.x, self.y),
            'cdata': self.cdata,
            'badbdd': Decrypt(os.path.join(js_path, 'badbdd.js')).decrypt_badbdd(mouse),
            'websig': self.websig,
            'fpinfo': 'fpsig=11006844CF33F90A84E31A9A1FFF3023D7E4B60E4E417FAC4E94327529ABBBD049BA32DAB50503D162BB83FCB22C701ABA2A',
            'tlg': '1',
            'vlg': '0_0_0',
            'vmtime': '_',
            'vmData': '',
        }
        r = self.parent.fetch(self.post_url, data=data)
        r.encoding = 'utf-8'
        return r.json()

    def captch(self):
        return self.fetch_captch()


class QQ:
    xlogin_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin'
    login_url = 'https://ssl.ptlogin2.qq.com/login'
    auth_url = 'https://graph.qq.com/oauth2.0/authorize'

    def __init__(self, qq='', password='', third_url='', qr=False):
        self.session = requests.Session()
        self.qq = qq
        self.password = password
        self.third_url = third_url
        self.qr = qr
        self.verifier = Verify(self)

    def fetch(self, url, data=None, **kwargs):
        if data:
            kwargs['data'] = data
            func = self.session.post
        else:
            func = self.session.get
        return func(url, **kwargs)

    @property
    def __fetch_jumpurl(self):
        hosts = re.search('http[s]?://(.*?)/', self.third_url)[1]
        headers = {
            'Host': hosts,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.56 Safari/537.36',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pl;q=0.7,fr;q=0.6',
        }
        r = self.fetch(self.third_url, headers=headers, allow_redirects=False)
        self.r = r
        if r.status_code == 302 or r.status_code == 301:
            url = r.headers['Location']  # 获取跳转链接
        else:
            url = re.findall("\'(https://graph.qq.com.*?)\'", r.text)[0]
        return url

    @property
    def _fetch_qr(self):
        '''
        二维码登录
        :return:二维码路径
        '''
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        res = self.fetch(url, params={
            'aid': self.param['param']['appid'],
            'daid': self.param['param']['daid'],
            'pt_3rd_aid': self.param['param']['pt_3rd_aid'],
        })

        tmp = tempfile.mkstemp(suffix='.jpg')
        os.write(tmp[0], res.content)
        os.close(tmp[0])
        return tmp[1]

    def __fetch_param(self, url):
        param = {}
        response = self.fetch(url, verify=False).text
        param.update({'appid': re.findall('appid=(\d+)&', response)[0]})
        param.update({'daid': re.findall('daid=(\d+)&', response)[0]})
        param.update({'style': re.findall('style=(\d+)&', response)[0]})
        param.update({'login_text': re.findall('login_text=(.*?)&', response)[0]})
        param.update({'hide_title_bar': re.findall('hide_title_bar=(\d+)&', response)[0]})
        param.update({'hide_border': re.findall('hide_border=(\d+)&', response)[0]})
        param.update({'target': re.findall('target=(.*?)&', response)[0]})
        param.update({'s_url': re.findall('var s_url = \'(.*?)\';', response)[0]})
        client_id = re.findall('client_id=(\d+)', url)[0]
        redirect_uri = re.findall('redirect_uri=(.*?)&', url)[0]
        redirect_uri = urllib.parse.unquote(redirect_uri)
        hosts = re.findall('//(.*?)/', redirect_uri)[0]
        param.update({'pt_3rd_aid': client_id})
        param.update({'pt_feedback_link': 'http://support.qq.com/write.shtml?fid=780&SSTAG=%s.appid%s' % (
            hosts, param['appid'])})
        canshu = urllib.parse.urlsplit(url).query
        res = urllib.parse.parse_qs(canshu)
        dicts = dict([(key, val[0]) for key, val in res.items()])
        state = dicts['state'] if 'state' in dicts else ''
        scope = dicts['scope'] if 'scope' in dicts else ''
        return {'param': param, 'client_id': client_id, 'redirect_url': dicts['redirect_uri'],
                'state': state, 'scope': scope}

    def xlogin(self, param):
        self.fetch(self.xlogin_url, params=param, verify=False)

    def _fetch_jumpurl(self, res):
        logger.info('QQ: %s 成功登陆，昵称：%s' % (self.qq, res['nickname']))
        self.fetch(res['jump_url'])
        self.fetch('https://graph.qq.com/oauth2.0/login_jump')
        data = {
            'response_type': 'code',
            'client_id': self.param['client_id'],
            'redirect_uri': self.param['redirect_url'],
            'scope': self.param['scope'],
            'state': self.param['state'],
            'switch': '',
            'from_ptlogin': '1',
            'src': '1',
            'update_auth': '1',
            'openapi': '80901010',
            'g_tk': self.gettoken,
            'auth_time': int(time.time() * 1000),
            'u1': '54A6E5F9-26E8-45EA-BBDD-49245AF3B140'
        }
        print(data)
        r = self.fetch(self.auth_url, allow_redirects=False, data=data)
        urls = r.headers['Location']
        logger.info('跳转链接：%s' % urls)
        return {'error': 0, 'info': urls, 'qq': self.qq, 'nickname': res['nickname'], 'cookies': self.r.cookies}

    @property
    def login(self):
        jump_qq_url = self.__fetch_jumpurl  # 第三方跳转
        self.param = self.__fetch_param(jump_qq_url)
        print(self.param)
        self.xlogin(self.param['param'])
        if self.verifier.check()[0] == '1':
            # 需要滑块验证码
            for i in range(3):
                res = Captch(self).captch()
                if self.verifier.checkCaptch(res):
                    break
                else:
                    logger.error('验证码错误，重试次数-----%d' % (i + 1))

        ptvfsession = self.verifier.ptvfsession or self.session.cookies.get('ptvfsession', '')
        password = Decrypt(os.path.join(js_path, 'pwd.js')).decrypt_pwd(self.password, self.qq, self.verifier.vcode)
        params = {
            'u': self.qq,
            'verifycode': self.verifier.vcode,
            'pt_vcode_v1': self.verifier.pt_vcode_v1,
            'pt_verifysession_v1': ptvfsession,
            'p': password,
            'pt_randsalt': '2',
            'u1': 'https://graph.qq.com/oauth2.0/login_jump',
            'ptredirect': '0', 'h': '1', 't': '1', 'g': '1',
            'from_ui': '1', 'ptlang': '2052',
            'action': '8-13-1651821569623',
            'js_ver': '22042810', 'js_type': '1',
            'login_sig': self.session.cookies['pt_login_sig'],
            'pt_uistyle': '40',
            'aid': self.param['param']['appid'],
            'daid': self.param['param']['daid'],
            'pt_3rd_aid': self.param['client_id'],
            'ptdrvs': self.session.cookies['ptdrvs'],
            'sid': self.verifier.sid,
            'o1vId': 'c49b27c5674cf61587a47928903f7219'
        }
        r = self.fetch(self.login_url, params=params, headers=headers)
        verify_res = self.verifier.verify_islogin(r.text)
        if verify_res['error'] == 0:
            # 成功登陆
            return self._fetch_jumpurl(verify_res)
        elif verify_res['error'] == 3 and self.qr is True:
            # 账号密码错误，扫码登录
            qr_path = self._fetch_qr
            logger.error('QQ: %s 成功获取二维码，二维码路径：%s，请调用login_qr方法' % (self.qq, qr_path))
            return {'error': 110, 'info': qr_path}
        logger.error('QQ: %s 登陆失败，信息：%s' % (self.qq, verify_res['info']))
        return verify_res

    def login_qr(self):
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
        params = {
            'login_sig': self.cookies.get('pt_login_sig'),
            'aid': self.param['param']['appid'],
            'ptqrtoken': self._hash(self.cookies.get('qrsig')),
            'action': '5-36-1521202241770',
            'ptredirect': 0,
            'js_ver': 10270,
            'js_type': 1,
            'g': 1,
            'from_ui': 1,
            't': 1,
            'pt_uistyle': 40,
            'h': 1,
            'daid': self.param['param']['daid'],
            'u1': 'https://graph.qq.com/oauth2.0/login_jump'
        }
        while True:
            r = self.fetch(url, params=params)
            matches = re.findall('\'(.*?)\'', r.text)
            if matches[0] == '66':
                # 未失效
                logger.info('二维码未失效，等待扫描')
                time.sleep(2)
                continue
            elif matches[0] == '67':
                # 等待认证
                logger.info('等待认证中')
                time.sleep(2)
                continue
            elif matches[0] == '65':
                logger.info('二维码已失效')
                return {'error': 111, 'info': '二维码已失效'}
            else:
                # os.popen('taskkill /IM dllhost.exe')
                verify_res = self.verifier.verify_islogin(r.text)
                return self._fetch_jumpurl(verify_res)

    @property
    def cookies(self):
        return self.session.cookies

    @property
    def gettoken(self):
        cur_cookies = self.cookies
        if 'skey' in cur_cookies:
            s_key = self.cookies.get('skey')
        else:
            s_key = self.cookies.get('p_skey')
        hash_code = 5381
        for i in s_key:
            t = (hash_code << 5) + ord(i)
            hash_code = hash_code + t
        return hash_code & 0x7fffffff

    def _hash(self, str1):
        i = 0
        for x in str1:
            i += (i << 5) + ord(x)
        return 2147483647 & i


if __name__ == '__main__':
    qq = "***"
    p = '***'
    third_url = 'https://cloud.tencent.com/login/qqConnect?s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fcat%2Fprobe%2Ftasklist&fwd_flag=7'
    qq = QQ(third_url=third_url, qq=qq, password=p)
    print(qq.login)
