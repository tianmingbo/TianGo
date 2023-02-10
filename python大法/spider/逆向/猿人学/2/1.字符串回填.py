# test.py
import copy
import json
import os
import sys

import requests
import execjs

""" 字符串与数字回填 """
string_number_dict = {}


def get_js():
    res = requests.get('https://match.yuanrenxue.com/match/2')
    with open('./ob.js', 'wb') as f:
        f.write(res.content[8:-9])
    os.system('node JsToJson ob.js ob.json')

    # 总文件分为6个部分,将前三个与后三个部分拆开
    with open('./ob.json', 'r', encoding='utf8') as f:
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
    with open('original_left.json', 'w', encoding='utf8') as f1, open('original_right.json', 'w',
                                                                      encoding='utf8') as f2:
        f1.write(json.dumps(left_3_node))
        f2.write(json.dumps(right_3_node))

    os.system('node JsonToJs original_left.json original_left.js')
    os.system('node JsonToJs original_right.json original_right.js')


def test_get_value():
    with open('original_left.js', 'r', encoding='utf-8') as f:
        ctx = execjs.compile(f.read())
    res = ctx.call('$dbsm_0x42c3', '0x43a', 'PjOm') + 'rr'
    print(res)


# 提取变量与字符串的映射
def get_string_number_dict(data, index):
    # 后三部分,每一部分都有这样的结构,而且变量名称有重复,必须分开做
    string_number_dict.clear()
    if index == 0:
        expressions_list = data[index]['expression']['callee']['body']['body'][0]['expression']['expressions']
    elif index == 1:
        expressions_list = data[index]['body']['body'][0]['expression']['expressions']
    else:
        expressions_list = data[index]['expression']['arguments'][0]['body']['body'][0]['expression'][
            'expressions']

    for item in expressions_list:
        if item['type'] != 'AssignmentExpression':
            continue
        if item['left']['type'] == 'Identifier':
            if item['right']['type'] == 'Literal':
                string_number_dict[item['left']['name']] = item['right']
            elif item['right']['type'] == 'BinaryExpression':
                left = string_number_dict[item['right']['left']['name']]
                right = item['right']['right']
                try:
                    new_node = copy.deepcopy(right)
                    new_node['value'] = eval(f'{left["value"]} {item["right"]["operator"]} {right["value"]}')
                    string_number_dict[item['left']['name']] = new_node
                except TypeError:
                    print(item['right'])
                    sys.exit()


def string_number_reload(node):
    # 一次只能还原一个部分
    if type(node) == list:
        # 虽然arguments 自身就是一个列表,但是他会在下方被捕捉,不会进入这个递归分支
        for item in node:
            string_number_reload(item)
        return
    elif type(node) != dict:  # 不是容器类型,就停止递归
        return
    # 捕捉一个包含 arguments 属性的节点
    try:
        for i in range(len(node['arguments'])):  # 遍历所有参数
            if node['arguments'][i]['type'] == 'Identifier':  # 匹配,则进入替换分支
                try:
                    node['arguments'][i] = string_number_dict[node['arguments'][i]['name']]
                except KeyError:
                    pass
        else:
            raise KeyError
    except KeyError:  # 从根往下遍历
        for key in node.keys():
            string_number_reload(node[key])
        return


# 删除变量声明
def del_string_number_node(data, index):
    if index == 0:
        expressions_list = data[index]['expression']['callee']['body']['body'][0]['expression']['expressions']
    elif index == 1:
        expressions_list = data[index]['body']['body'][0]['expression']['expressions']
    else:
        expressions_list = data[index]['expression']['arguments'][0]['body']['body'][0]['expression'][
            'expressions']
    for i in range(len(expressions_list) - 1, -1, -1):
        if expressions_list[i]['type'] != 'AssignmentExpression':
            continue
        if expressions_list[i]['left']['type'] == 'Identifier' and expressions_list[i]['right']['type'] in (
                'Literal', 'BinaryExpression'):
            del expressions_list[i]


if __name__ == '__main__':
    get_js()
    # test_get_value()
    with open('original_right.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    for i in range(len(data['body'])):  # 将每一部分,分别做回填
        get_string_number_dict(data['body'], i)
        string_number_reload(data['body'][i])
        del_string_number_node(data['body'], i)
    with open('mid1.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs mid1.json mid1.js')
