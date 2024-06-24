import copy
import json
import os
import sys

import requests
import execjs


def get_02_ob_js():
    res = requests.get('https://match.yuanrenxue.com/match/2')
    with open('./02_ob.js', 'wb') as f:
        f.write(res.content[8:-9])
    os.system('node JsToJson 02_ob.js 02_ob.json')

    # 总文件分为6个部分,将前三个与后三个部分拆开
    with open('./02_ob.json', 'r', encoding='utf8') as f:
        node = json.loads(f.read())
    left_3_node = {
        'type': 'Program',
        'body': node['body'][:3],
        'sourceType': 'script'
    }
    right_3_node = {
        'type': 'Program',
        'body': node['body'][3:],
        'sourceType': 'script'
    }
    with open('original_left.json', 'w', encoding='utf8') as f1, open('02_ob_right_3.json', 'w', encoding='utf8') as f2:
        f1.write(json.dumps(left_3_node))
        f2.write(json.dumps(right_3_node))

    os.system('node JsonToJs original_left.json original_left.js')
    os.system('node JsonToJs 02_ob_right_3.json 02_ob_right_3.js')


def test_get_value():
    with open('original_left.js', 'r', encoding='utf-8') as f:
        ctx = execjs.compile(f.read())
    res = ctx.call('$dbsm_0x42c3', '0x2ac', 'lDFj') + 'gw'
    print(res)


if __name__ == '__main__':
    # get_02_ob_js()
    test_get_value()
