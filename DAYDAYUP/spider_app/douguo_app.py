import json

import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; V1813BT Build/PKQ1.181030.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36',
    'Host': 'api.douguo.net'

}


def handle_request(url):
    res = requests.post(url, headers=header)
    text = res.text
    print(text)


if __name__ == '__main__':
    url = 'https://api.douguo.net/search/universalnew/0/10'
    handle_request(url)
