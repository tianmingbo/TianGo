import copy
import json
import os

obj_property_dict = {}
obj_name_list = []


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
                        i['init']['type'] == 'ObjectExpression':
                    if i['id']['name'] not in obj_property_dict:
                        obj_property_dict[i['id']['name']] = {}
                    for j in i['init']['properties']:
                        obj_property_dict[i['id']['name']][j['key']['value']] = j['value']
                    # i.clear()
                    # i.update({"type": 'EmptyStatement'})
    except KeyError as e:
        pass
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
    # 捕获一个属性调用节点
    try:
        if node['type'] == 'MemberExpression':
            # 处理形似：_0x5243e3['UhBgk']
            obj_name = node['object']['name']
            obj_property = node['property']['value']
            new_node = obj_property_dict[obj_name][obj_property]
            if new_node['type'] != 'FunctionExpression':
                node.clear()
                node.update(new_node)
                obj_property_reload(node)
    except KeyError:
        pass

    try:
        # 捕获一个函数调用节点,且子节点callee的类型是一个MemberExpression
        if node['type'] != 'CallExpression' or node['callee']['type'] != 'MemberExpression':
            raise KeyError
        obj_name = node['callee']['object']['name']  # 获取对象名称
        obj_property_name = node['callee']['property']['value']  # 获取需要调用的对象属性名称
        function_node = obj_property_dict[obj_name][obj_property_name]  # 获取函数定义节点,即对象的属性值(该属性值是一个函数定义)
    except KeyError:
        for key in node.keys():
            obj_property_reload(node[key])
        return

    # 获取形参
    param_list = [item['name'] for item in function_node['params']]
    # 获取实参
    argument_list = node['arguments']
    try:
        for k in argument_list:
            if k['name'] == 'define' or k['name'] == 'exports':
                return
    except Exception:
        pass
    # 形成形参与实参的对比关系,如此,可以适应形参位置发生变化
    param_argument_dict = dict(zip(param_list, argument_list))
    # 拷贝一份函数节点的返回值子节点
    return_node = copy.deepcopy(function_node['body']['body'][0])
    # print(return_node)
    if return_node['type'] == 'FunctionExpression' and not node['id']:
        print(f'意料之外的函数节点,拥有超过一行的函数体: {function_node}')
        # for key in node.keys():
        #     obj_property_reload(node[key])
        return
    # 使用实参替换返回值节点中的形参,然后用返回值节点,替换掉整个函数调用node节点
    print(return_node)
    try:
        if return_node['argument']['type'] == 'BinaryExpression' or \
                return_node['argument']['type'] == 'LogicalExpression':
            if return_node['argument']['left']['type'] == 'Identifier':
                return_node['argument']['left'] = param_argument_dict[return_node['argument']['left']['name']]
            if return_node['argument']['right']['type'] == 'Identifier':
                return_node['argument']['right'] = param_argument_dict[return_node['argument']['right']['name']]
            node.clear()
            node.update(return_node['argument'])
        elif return_node['argument']['type'] == 'CallExpression':
            # 处理形似return _0x1debf7['rDkzY'](_0x3106cb, _0x48a349)
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
        # else:
        #     print(f'意料之外的函数返回值类型: {return_node}')
        #     sys.exit()
        # 替换完成后,将自身继续递归
    except Exception:
        pass
    for key in node.keys():
        obj_property_reload(node[key])


if __name__ == '__main__':
    with open('udc_mid1.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    get_property_dict(data)
    obj_property_reload(data)
    with open('udc_mid2.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs udc_mid2.json udc_mid2.js')
