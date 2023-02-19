import json
import os
import re
import subprocess
import execjs
import requests

node = execjs.get()

session = requests.session()

headers = {'User-Agent': 'yuanrenxue.project'}
sum_num = 0


def login():
    data = {
        'username': 'chendali',
        'password': '********'
    }
    session.post('https://match.yuanrenxue.com/api/login', data=data)
    session.get('https://match.yuanrenxue.com/api/loginInfo')


def get_v():
    """
    get v14 and v142
    :return:
    """
    res = session.get('https://match.yuanrenxue.com/api/match/14/m')
    v = re.findall("window\[\${0,1}.*?=(\${0,1}.*?);", res.text)
    if len(v) != 2:
        get_v()
    with open('./m.js', 'wb') as f:
        f.write(res.content)
    os.system('/usr/local/bin/node JsToJson m.js m.json')
    with open('./m.json', 'r', encoding='utf8') as f:
        node = json.loads(f.read())
    array_revert_node = {
        'type': 'Program',
        'body': node['body'][:3],
        'sourceType': 'script'
    }
    with open('m_array_revert.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(array_revert_node))
    os.system('/usr/local/bin/node JsonToJs m_array_revert.json m_array_revert.js')
    return v


def get_cookie(page_num, v):
    with open('m_array_revert.js', 'r', encoding='utf-8') as f:
        ctx = node.compile(f.read())
    v = [ctx.eval(i) for i in v]
    p = subprocess.Popen(['/usr/local/bin/node', './mz6.js', str(page_num), v[0], v[1]], stdout=subprocess.PIPE)
    m = p.stdout.read().decode('UTF-8').replace('\n', '')
    cookies = {
        'mz': 'TW96aWxsYSxOZXRzY2FwZSw1LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTVfNykgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMC4wLjAuMCBTYWZhcmkvNTM3LjM2LFtvYmplY3QgTmV0d29ya0luZm9ybWF0aW9uXSx0cnVlLCxbb2JqZWN0IEdlb2xvY2F0aW9uXSw4LHpoLUNOLHpoLUNOLHpoLDAsW29iamVjdCBNZWRpYUNhcGFiaWxpdGllc10sW29iamVjdCBNZWRpYVNlc3Npb25dLFtvYmplY3QgTWltZVR5cGVBcnJheV0sdHJ1ZSxbb2JqZWN0IFBlcm1pc3Npb25zXSxNYWNJbnRlbCxbb2JqZWN0IFBsdWdpbkFycmF5XSxHZWNrbywyMDAzMDEwNyxbb2JqZWN0IFVzZXJBY3RpdmF0aW9uXSxNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV83KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTEwLjAuMC4wIFNhZmFyaS81MzcuMzYsR29vZ2xlIEluYy4sLFtvYmplY3QgRGVwcmVjYXRlZFN0b3JhZ2VRdW90YV0sW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSw4NzUsMCwyNSwxNDQwLDMwLDkwMCxbb2JqZWN0IFNjcmVlbk9yaWVudGF0aW9uXSwzMCwxNDQwLFtvYmplY3QgRE9NU3RyaW5nTGlzdF0sZnVuY3Rpb24gYXNzaWduKCkgeyBbbmF0aXZlIGNvZGVdIH0sLG1hdGNoLnl1YW5yZW54dWUuY29tLG1hdGNoLnl1YW5yZW54dWUuY29tLGh0dHBzOi8vbWF0Y2gueXVhbnJlbnh1ZS5jb20vbWF0Y2gvMTQsaHR0cHM6Ly9tYXRjaC55dWFucmVueHVlLmNvbSwvbWF0Y2gvMTQsLGh0dHBzOixmdW5jdGlvbiByZWxvYWQoKSB7IFtuYXRpdmUgY29kZV0gfSxmdW5jdGlvbiByZXBsYWNlKCkgeyBbbmF0aXZlIGNvZGVdIH0sLGZ1bmN0aW9uIHRvU3RyaW5nKCkgeyBbbmF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gdmFsdWVPZigpIHsgW25hdGl2ZSBjb2RlXSB9',
        'm': m + str(page_num)
    }
    print(v)
    print(cookies)
    return cookies


def get_page_info():
    global sum_num
    url = 'https://match.yuanrenxue.com/api/match/14?'
    for i in range(1, 6):
        v = get_v()
        cookies = get_cookie(i, v)
        res = session.get(f'{url}page={i}', headers={'User-Agent': 'yuanrenxue.project'}, cookies=cookies).json()
        for j in res['data']:
            sum_num += j['value']


if __name__ == '__main__':
    login()
    get_page_info()
    print(sum_num)
