import os
import re
import execjs
import requests

"""
获取音乐
https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19102481978914731513_1672893430351&dfid=0jIRr704C50U1yIiAx3JgEWz&appid=1014&mid=e52a05c3f3cf79c19b9ffcab4c187bed&platid=4&encode_album_audio_id=7ssttec0&_=1672893430352
registerDev.v1.min.js?appid=1014&20190408:formatted 1094 debugger
"""
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}


class KuGou:
    def __init__(self):
        self.session = requests.Session()
        self.key_params = self.get_key_params()

    def fetch(self, url, data=None, **kwargs):
        if data:
            kwargs['data'] = data
            func = self.session.post
        else:
            func = self.session.get
        return func(url, **kwargs)

    @staticmethod
    def read_file(path):
        node = execjs.get()
        with open(path, "r", encoding="utf-8") as f:
            return node.compile(f.read())

    def get_key_params(self):
        ctx = self.read_file('kg_mid_dfid.js')
        return ctx.call('getUrlDfid')

    def get_dfid(self):
        print(self.key_params['register_url'], self.key_params['fingerPrint'])
        dfid = self.fetch(self.key_params['register_url'], data=self.key_params['fingerPrint'], headers=headers)
        return dfid.json()['data']['dfid']


song_par = re.compile('"play_url":"(.*?)","au', re.I | re.M)

if __name__ == '__main__':
    kugou = KuGou()

    url = 'https://wwwapi.kugou.com/yy/index.php'
    param = {
        'r': 'play/getdata',
        'callback': 'jQuery191049889224078365313_1672839068389',
        'dfid': kugou.get_dfid(),
        'appid': '1014',
        'mid': kugou.key_params['kg_mid'],
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
