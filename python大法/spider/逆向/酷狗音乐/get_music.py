import os
import re

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}

song_par = re.compile('"play_url":"(.*?)","au', re.I | re.M)
hash_pat = re.compile('"Hash":"(.*?)".*?"album_id":(.*?),"encrypt_id', re.I | re.M)
index_url = requests.get('https://www.kugou.com/yy/html/rank.html', headers=headers)
hashs = re.findall(hash_pat, index_url.text)
print(hashs)

# for h in hashs:
url = 'https://wwwapi.kugou.com/yy/index.php'
# url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191049889224078365313_1672839068389&dfid=2mSjyM2i31kI0j5orH1ipSln&appid=1014&mid=938333539676f5768374176fe3f69cfa&platid=4&encode_album_audio_id=7qmtwabe&_=1672839068390'
param = {
    'r': 'play/getdata',
    'callback': 'jQuery191049889224078365313_1672839068389',
    'dfid': '2mSjyM2i31kI0j5orH1ipSln',
    'appid': '1014',
    'mid': '938333539676f5768374176fe3f69cfa',
    'platid': '4',
    'encode_album_audio_id': '7qmtwabe',
    '_': '1672839068390'
}
song = requests.get(url, headers=headers, params=param)
print(song.text)
for i in re.findall(song_par, song.text):
    song_play_url = i.replace('\/', '/')
    print(song_play_url)

if not os.path.exists('./song'):
    os.mkdir('./song')

with open('./song/{}'.format(song_play_url[-10:]), 'wb') as f:
    f.write(requests.get(song_play_url).content)
