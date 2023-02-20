import httpx


sum_num = 0
headers = {
    'cookie': 'no-alert3=true; tk=-8476045948478067908; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1676684794,1676713265; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1676690110,1676713374,1676797454; sessionid=lfymkud2zd7tkzj0sqtgjo6si8rp0tpi; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1676867431; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1676867444',
    'User-Agent': 'yuanrenxue.project'
}


def get_page_info():
    global sum_num
    url = 'https://match.yuanrenxue.com/api/match/17?'
    with httpx.Client(headers=headers, http2=True) as client:
        for i in range(1, 6):
            params = {
                'page': i,
            }
            res = client.get(f'{url}page={i}', params=params)
            print(res.text)
            res = res.json()
            for val in res['data']:
                sum_num += val['value']


if __name__ == '__main__':
    get_page_info()
    print(sum_num)
