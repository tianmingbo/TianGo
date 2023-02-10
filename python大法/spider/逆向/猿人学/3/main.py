import requests
import urllib3
from collections import Counter

urllib3.disable_warnings()

headers = {
    "Content-Length": "0",
    "sec-ch-ua-platform": "Windows",
    "Accept": "*/*",
    "Referer": "https://match.yuanrenxue.com/match/3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "m=e6370aff58adacf77e6ddbbe8b365047|1659771468000; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1659761954,1659767697,1659767716,1659771472; qpfccr=true; no-alert3=true; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1659443435,1659452878,1659761832,1659771825; tk=-3495643738000386252; sessionid=wob9s7wdgrmmsnb7o8cl3a0ycqhmi9lf; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1659771870; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1659771870",
}


def get_page_info():
    res_list = []
    url = 'http://match.yuanrenxue.com/api/match/3?'
    for i in range(1, 6):
        if i == 4 or i == 5:
            headers['user-agent'] = 'yuanrenxue.project'
        session.headers = headers
        session.post("https://match.yuanrenxue.com/jssm")
        response = session.get(f'{url}page={i}').json()
        for val in response['data']:
            res_list.append(val['value'])
    return res_list


if __name__ == '__main__':
    session = requests.session()
    res = get_page_info()
    print(Counter(res).most_common(1))
