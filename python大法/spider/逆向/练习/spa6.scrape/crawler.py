# https://spa6.scrape.center/page/9
import requests
import time
import hashlib
import base64

INDEX_URL = 'https://spa6.scrape.center/api/movie?limit={limit}&offset={offset}&token={token}'
DETAIL_URL = 'https://spa6.scrape.center/api/movie/{id}?token={token}'
LIMIT = 10
OFFSET = 0
SECRET = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'


def get_token(detail_flag=False, secret_id=None):
    timestamp = str(int(time.time()))
    args = ['/api/movie', timestamp]
    if detail_flag:
        args = [f'/api/movie/{secret_id}', timestamp]
    time.sleep(1)
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()  # sha1加密
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')  # base64


def get_detail(id):
    encrypt_id = base64.b64encode((SECRET + str(id)).encode('utf-8')).decode('utf-8')
    token = get_token(True, encrypt_id)
    url = DETAIL_URL.format(id=encrypt_id, token=token)
    res = requests.get(url)
    print(res.json())


def get_page_info():
    for i in range(10):
        token = get_token()
        url = INDEX_URL.format(limit=LIMIT, offset=i * LIMIT, token=token)
        res = requests.get(url)
        for detail_id_info in res.json()['results']:
            get_detail(detail_id_info['id'])
            break


if __name__ == '__main__':
    get_page_info()
