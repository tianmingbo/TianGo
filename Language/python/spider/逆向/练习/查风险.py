"""
http://cfx.health.xywy.com/question/1/index.htm
获取报表
csrf从开始返回文件中拿到
"""
import re

import requests

headers = {
    'Host': 'cfx.health.xywy.com',
    'Referer': 'http://cfx.health.xywy.com/',
    'Origin': 'http://cfx.health.xywy.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'cookie': '',
}


def get_csrf():
    csrf_url = 'http://cfx.health.xywy.com/question/1/index.htm'
    global headers
    res = requests.get(csrf_url, headers=headers)
    for k, v in res.cookies.items():
        headers['cookie'] += k + '=' + v + ';'
    csrf = re.findall(re.compile('name="_csrf"\svalue="(.*?)"\s/>'), res.text)[0]
    return csrf


def get_report(csrf):
    report_url = 'http://cfx.health.xywy.com/question/1/index.htm'
    params = f'_csrf={csrf.replace("=", "")}%3D%3D&params%5Bage%5D=22&params%5Bgender%5D=1&params%5Bhbp_his%5D=1&params%5Bdiab_his%5D=1&params%5Bdiab_family%5D=1&params%5Bsmoke_status%5D=1&params%5Bvegetable%5D=1&params%5Bfru%5D=1&params%5Bis_act%5D=1&params%5Bact_freq%5D=1&params%5Bact_time%5D=1&params%5Bact_intensity%5D=1&params%5Bwaist%5D=77.0&params%5Btg%5D=12.00&params%5Bhdl%5D=12.00&params%5Bheight%5D=178.0&params%5Bweight%5D=78.00&params%5Bfbg%5D=34.00'
    print(headers)
    res = requests.post(report_url, headers=headers, data=params)
    # print(res.text)


if __name__ == '__main__':
    csrf = get_csrf()
    get_report(csrf)
