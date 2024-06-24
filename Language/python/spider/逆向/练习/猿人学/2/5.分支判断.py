import json
import os
import sys

operator_dict = {'===': '==', '!==': '!='}


def if_reload(node):
    if type(node) == list:
        for item in node:
            if_reload(item)
        return
    elif type(node) != dict:
        return

    # 捕获一个分支语句节点
    if node['type'] == 'IfStatement':
        if node['test']['type'] == 'BinaryExpression':
            # 判断分支条件是否可执行
            if node['test']['left']['type'] == 'Literal' and node['test']['right']['type'] == 'Literal':
                # 获取分支节点
                consequent = node['consequent']
                alternate = node['alternate']
                try:
                    if eval(f"'{node['test']['left']['value']}' {operator_dict[node['test']['operator']]} '{node['test']['right']['value']}'"):
                        node.clear()
                        node.update(consequent)
                    else:
                        node.clear()
                        node.update(alternate)
                except KeyError:
                    print(f'意料之外的分支运算符号: {node}')
                    sys.exit()
                else:
                    if_reload(node)
    for key in node.keys():
        if_reload(node[key])


if __name__ == '__main__':
    with open('mid5.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    if_reload(data)

    with open('mid6.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs mid6.json mid6.js')
