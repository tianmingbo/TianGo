"""
浏览器指纹：771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,45-16-65281-11-0-10-27-17513-23-18-35-43-13-5-51,29-23-24,0
requests 指纹：771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49161-49187-49171-49191-49162-49188-49172-49192-49160-49170-156-157-47-60-53-61-10,0-23-65281-10-11-35-16-5-13-13172-18-51-45-43-21,29-23-24,0

"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)

headers = {
    'user-agent': 'yuanrenxue.project',
    'cookie': 'sessionid=lfymkud2zd7tkzj0sqtgjo6si8rp0tpi;'
}


class DESAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


def get_page_info(s):
    num_sum = 0
    for i in range(1, 6):
        r = s.get(f'https://match.yuanrenxue.com/api/match/19?page={i}', headers=headers)
        print(r.text)
        res = r.json()
        print(res)
        data = res.get('data')
        num_sum += sum([int(d.get('value')) for d in data])
    print('num_sum', num_sum)


if __name__ == '__main__':
    s = requests.Session()
    s.mount('https://match.yuanrenxue.com', DESAdapter())
    get_page_info(s)
