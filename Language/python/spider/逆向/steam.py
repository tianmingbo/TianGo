import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer': 'https://store.steampowered.com/login/?redir=about&redir_ssl=1&snr=1_14_4__global-header'
}
data = {
    'username': '123456',
    'donotcache': int(time.time() * 1000)
}
url = 'https://store.steampowered.com/login/getrsakey/'
res = requests.post(url, data=data, headers=headers)
print(res.text)
print(res.status_code)
