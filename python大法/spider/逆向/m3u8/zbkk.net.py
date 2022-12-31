import requests

m3u = []
res = requests.get('https://vip.lzcdn2.com/20221226/22951_30233da1/1800k/hls/mixed.m3u8')
for i in res.text.split('\n'):
    if 'bcf695' in i:
        m3u.append(i)
file = open(r'C:\Users\mingbotian\Desktop\afw.mp4', 'wb+')
base_url = 'https://vip.lzcdn2.com/20221226/22951_30233da1/1800k/hls/'
print(len(m3u))
for i in m3u:
    print(i)
    file.write(requests.get(base_url + i).content)
file.close()
