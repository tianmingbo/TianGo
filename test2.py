import requests

headers = {
    'Host': 'cat-match.easygame2021.com',
    'charset': 'utf-8',
    't': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ0ODI0MzQsIm5iZiI6MTY2MzM4MDIzNCwiaWF0IjoxNjYzMzc4NDM0LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo2MDE3NTc0MywiZGVidWciOiIiLCJsYW5nIjoiIn0.2uMbJkZffnQvyPOHw7TeDJohNS9yhKdU_I-uIkS1bYA',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Nexus 5X Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/8419 MicroMessenger/8.0.27.2220(0x28001B59) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/19/page-frame.html',
}

params = {
    'rank_score': '10',
    'rank_state': '10',
    'rank_time': '190',
    'rank_role': '10',
    'skin': '10',
}

response = requests.get('https://cat-match.easygame2021.com/sheep/v1/game/game_over', params=params, headers=headers)

print(response.text)