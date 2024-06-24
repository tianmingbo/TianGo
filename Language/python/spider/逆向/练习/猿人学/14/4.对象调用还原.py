import copy
import json
import os

obj_name_list = []
obj_property_dict = {}


def get_property_dict(node):
    global obj_property_dict
    if type(node) == list:
        for item in node:
            get_property_dict(item)
        return
    elif type(node) != dict:
        return
    if 'type' in node and node['type'] == 'BlockStatement':
        try:
            if len(node['body']) >= 3 and \
                    node['body'][0]['type'] == 'VariableDeclaration' and \
                    node['body'][1]['type'] == 'ExpressionStatement' and \
                    node['body'][2]['type'] == 'VariableDeclaration':
                obj_property_dict.clear()
                if 'init' in node['body'][2]['declarations'][0] and \
                        node['body'][2]['declarations'][0]['init']['type'] == 'Identifier':
                    obj_name = node['body'][2]['declarations'][0]['id']['name']
                    if obj_name not in obj_property_dict:
                        obj_property_dict[obj_name] = {}
                    for i in node['body'][1]['expression']['expressions']:
                        if i['type'] == 'AssignmentExpression':
                            property_name = i['left']['property']['value']
                            obj_property_dict[obj_name][property_name] = i['right']
                    obj_property_reload(node)
                    node['body'][2]['declarations'][0]['init'] = {'type': 'Literal', 'value': 'Nothing'}
                    node['body'] = node['body'][2:]
        except KeyError as e:
            print('error', e, node['body'][2]['declarations'])
    for key in node.keys():
        get_property_dict(node[key])


# 对象调用还原
def obj_property_reload(node):
    if type(node) == list:
        for item in node:
            obj_property_reload(item)
        return
    elif type(node) != dict:
        return
    try:
        if node['type'] == 'MemberExpression':
            # 处理形似：_0x5243e3['UhBgk']
            try:
                obj_name = node['object']['name']
                obj_property_name = node['property']['value']
                new_node = obj_property_dict[obj_name][obj_property_name]
                if new_node['type'] != 'FunctionExpression':
                    node.clear()
                    node.update(new_node)
            except Exception:
                pass
        # 捕获一个函数调用节点,且子节点callee的类型是一个MemberExpression
        if node['type'] == 'CallExpression' and node['callee']['type'] == 'MemberExpression':
            argument_list = node['arguments']
            for para in argument_list:
                if para['type'] == 'CallExpression':  # 递归调用
                    obj_property_reload(para)
            obj_name = node['callee']['object']['name']
            obj_property_name = node['callee']['property']['value']  # 获取需要调用的对象属性名称
            function_node = obj_property_dict[obj_name][obj_property_name]  # 获取函数定义节点,即对象的属性值(该属性值是一个函数定义)
            # 获取形参
            param_list = [item['name'] for item in function_node['params']]
            # 获取实参
            param_argument_dict = dict(zip(param_list, argument_list))
            return_node = copy.deepcopy(function_node['body']['body'][0])
            # print(return_node)
            if return_node['argument']['type'] == 'BinaryExpression' or \
                    return_node['argument']['type'] == 'LogicalExpression':
                if return_node['argument']['left']['type'] == 'Identifier':
                    return_node['argument']['left'] = param_argument_dict[return_node['argument']['left']['name']]
                if return_node['argument']['right']['type'] == 'Identifier':
                    return_node['argument']['right'] = param_argument_dict[return_node['argument']['right']['name']]
                node.clear()
                node.update(return_node['argument'])
            elif return_node['argument']['type'] == 'CallExpression':
                if return_node['argument']['callee']['type'] != 'MemberExpression':
                    function_name = return_node['argument']['callee']['name']
                    if function_name in param_argument_dict:
                        return_node['argument']['callee'] = param_argument_dict[function_name]
                    for i in range(len(return_node['argument']['arguments'])):
                        if return_node['argument']['arguments'][i]['type'] == 'Identifier':
                            argument_name = return_node['argument']['arguments'][i]['name']
                            return_node['argument']['arguments'][i] = param_argument_dict[argument_name]
                node.clear()
                node.update(return_node['argument'])
    except Exception as e:
        print('???', e)
    for key in node.keys():
        obj_property_reload(node[key])


if __name__ == '__main__':
    with open('mz3.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    get_property_dict(data)
    print(obj_property_dict.keys())
    with open('mz4.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('/usr/local/bin/node JsonToJs mz4.json mz4.js')
