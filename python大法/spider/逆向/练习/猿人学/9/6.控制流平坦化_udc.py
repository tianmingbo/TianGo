import json
import os

obj_property_dict = {}


def get_property_dict(node):
    if type(node) == list:
        for item in node:
            get_property_dict(item)
        return
    elif type(node) != dict:
        return

    # 捕获一个表达式序列
    try:
        if node and node['type'] == 'VariableDeclaration':
            for i in node['declarations']:
                if i['type'] == 'VariableDeclarator' and i['init'] and \
                        i['init']['type'] == 'CallExpression':
                    if i['id']['name'] not in obj_property_dict:
                        obj_property_dict[i['id']['name']] = {}
                    obj_property_dict[i['id']['name']] = i['init']['callee']['object']['value']
                    # i.clear()
                    # i.update({"type": 'EmptyStatement'})
    except KeyError as e:
        pass
    for key in node.keys():
        get_property_dict(node[key])


def sort_code(node):
    if type(node) == list:
        try:
            # 捕获一个控制流节点(这是一个包含执行顺序和while节点的列表节点)
            if len(node) == 2:
                if node[1]['type'] == 'WhileStatement':
                    split_key = node[1]['body']['body'][0]['discriminant']['object']['name']
                    sort_list = obj_property_dict[split_key].split('|')
                    cases_list = node[1]['body']['body'][0]['cases']
                    result_list = [cases_list[int(i)]['consequent'][0] for i in sort_list]
                    node.clear()
                    node.extend(result_list)
            if len(node) == 3:
                if node[2]['type'] == 'WhileStatement':
                    split_key = node[2]['body']['body'][0]['discriminant']['object']['name']
                    sort_list = obj_property_dict[split_key].split('|')  # 控制流程顺序列表
                    cases_list = node[2]['body']['body'][0]['cases']  # 原控制流列表
                    result_list = [cases_list[int(i)]['consequent'][0] for i in sort_list]  # 新的控制流列表
                    node.clear()
                    node.extend(result_list)
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

    for item in node:
        sort_code(item)


if __name__ == '__main__':
    with open('udc_mid3.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    get_property_dict(data)
    sort_code(data)
    print(obj_property_dict)
    with open('udc_mid4.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs udc_mid4.json udc_mid4.js')
