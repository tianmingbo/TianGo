import requests

m3u = []
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
res = requests.get('https://vip.lz-cdn4.com/20230125/25602_14608b01/1800k/hls/mixed.m3u8')
for i in res.text.split('\n'):
    if '4bb02bb' in i:
        m3u.append(i)
file = open(r'./mjh.mp4', 'wb+')
base_url = 'https://vip.lz-cdn4.com/20230125/25602_14608b01/1800k/hls/'
print(len(m3u))
for i in m3u:
    print(i)
    file.write(requests.get(base_url + i, headers=headers).content)
file.close()
