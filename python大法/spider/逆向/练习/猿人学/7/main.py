"""
字体加密，发现on保持一致
"""
import base64
import requests
from fontTools.ttLib import TTFont

headers = {
    'Host': 'match.yuanrenxue.com',
    'Referer': 'http://match.yuanrenxue.com/match/6',
    'User-Agent': 'yuanrenxue.project',
}

number_woff_mapping = {
    '1010010010': '0', '1001101111': '1', '1001101010': '2', '1010110010': '3', '1111111111': '4',
    '1110101001': '5', '1010101010': '6', '1111111': '7', '1010101011': '8', '1001010100': '9'
}


def get_page(url):
    return requests.get(url=url, headers=headers).json()


def decode_base64(content):
    return base64.b64decode(content)


def write_woff(data, name):
    with open(f'{name}.woff', 'wb') as file:
        file.write(data)


def get_page_info(url, woff_file):
    response = get_page(url=url)
    res = [i['value'].replace('&#x', 'uni').split(' ') for i in response['data']]
    write_woff(data=decode_base64(content=response['woff']), name=woff_file)
    fonts = TTFont(f'{woff_file}.woff')
    fonts.saveXML(f'{woff_file}.xml')
    fonts.save(f'{woff_file}.TTF')
    for i in range(len(res)):
        for j in range(len(res[i])):
            tmp = ''
            if not res[i][j]:
                continue
            for k in fonts['glyf'][res[i][j]].flags[:10]:
                tmp += str(k)
            res[i][j] = number_woff_mapping[tmp]
        res[i] = int(''.join(res[i]))
    return res


if __name__ == '__main__':
    lp_l = []
    for page in range(1, 6):
        woff_file_name = f'woff_data{page}'
        url = f'http://match.yuanrenxue.com/api/match/7?page={page}'
        lp_l += get_page_info(url=url, woff_file=woff_file_name)
    print(max(lp_l))
