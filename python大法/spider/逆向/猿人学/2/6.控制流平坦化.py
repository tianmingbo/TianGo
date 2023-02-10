import json
import os
import sys


def sort_code(node):
    if type(node) == list:
        active = False
        try:
            # 捕获一个控制流节点(这是一个包含执行顺序和while节点的列表节点)
            if len(node) == 2:
                if node[1]['type'] == 'WhileStatement':
                    var1 = node[0]['expression']['expressions'][0]
                    var2 = node[0]['expression']['expressions'][1]
                    if var1['right']['type'] == 'CallExpression' and var2['right']['type'] == 'Literal':
                        active = True
            if not active:
                raise KeyError
        except (KeyError, TypeError):
            for item in node:
                sort_code(item)
            return
    elif type(node) == dict:
        for key in node.keys():
            sort_code(node[key])
        return
    else:
        return

    sort_list = var1['right']['callee']['object']['value'].split('|')  # 控制流程顺序列表
    cases_list = node[1]['body']['body'][0]['cases']  # 原控制流列表
    result_list = [cases_list[int(i)]['consequent'][0] for i in sort_list]  # 新的控制流列表

    node.clear()
    node.extend(result_list)
    for item in node:
        sort_code(item)


if __name__ == '__main__':
    with open('mid6.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    sort_code(data)
    with open('mid7.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs mid7.json final.js')
