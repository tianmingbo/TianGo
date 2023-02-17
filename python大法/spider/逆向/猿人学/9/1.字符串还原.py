import copy
import json
import os
import sys

import execjs

""" 字符串还原 """
string_number_dict = {}


def test_get_value():
    with open('original_left.js', 'r', encoding='utf-8') as f:
        ctx = execjs.compile(f.read())
    res = ctx.call('$dbsm_0x42c3', '0x43a', 'PjOm') + 'rr'
    print(res)


def string_reload(node):
    if type(node) == list:
        for item in node:
            string_reload(item)
        return
    elif type(node) != dict:
        return
    try:
        for i in range(len(node['arguments'])):
            if node['arguments'][i]['type'] == 'Identifier':
                try:
                    node['arguments'][i] = string_number_dict[node['arguments'][i]['name']]
                except KeyError:
                    pass
        else:
            raise KeyError
    except KeyError:  # 从根往下遍历
        for key in node.keys():
            string_reload(node[key])
        return


if __name__ == '__main__':
    with open('9_mid-1.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    string_reload(data)
    #
    os.system('node JsonToJs mid1.json mid1.js')
