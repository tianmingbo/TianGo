""" 对象调用还原 """

# 将拆分开的对象属性名称合并
import copy
import json
import os
import sys

# 构造对象属性字典
obj_property_dict = {}
obj_name_list = []


def get_property_dict(node):
    # 所有对象声明时都是: XXXX = {}, 然后使用 XXXX['xxxx'] = XXXXXXX 来添加属性
    if type(node) == list:
        for item in node:
            get_property_dict(item)
        return
    elif type(node) != dict:
        return

    # 捕获一个表达式序列
    if node['type'] == 'SequenceExpression':
        for i in range(- len(node['expressions']), 0, 1):  # 反向遍历列表,并且可以删除元素的方式
            item = node['expressions'][i]
            # 捕获一个(变量/属性)声明节点
            if item['type'] == 'AssignmentExpression':
                # 是一个变量声明
                if item['left']['type'] == 'Identifier':
                    # 声明的是一个空对象
                    if item['right']['type'] == 'ObjectExpression' and item['right']['properties'] == []:
                        obj_property_dict[item['left']['name']] = {}
                        obj_name_list.append(item['left']['name'])
                        del node['expressions'][i]
                        continue
                    # 声明 一个变量指向另一个变量 例: _0x5500bb = _0x434ddb,
                    elif item['right']['type'] == 'Identifier':
                        if item['right']['name'] in obj_property_dict:
                            obj_property_dict[item['left']['name']] = obj_property_dict[item['right']['name']]
                            obj_name_list.append(item['left']['name'])
                            del node['expressions'][i]
                            continue
                # 是一个属性声明
                elif item['left']['type'] == 'MemberExpression':
                    obj_name = item['left']['object']['name']
                    try:
                        obj_property_name = item['left']['property']['value']
                        obj_property_dict[obj_name][obj_property_name] = item['right']
                        del node['expressions'][i]
                        continue
                    except KeyError:
                        pass

            for key in item.keys():
                get_property_dict(item[key])

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
    if node['type'] == 'MemberExpression':
        try:
            # 处理形似：_0x5500bb['RmLGP']
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
    # 形成形参与实参的对比关系,如此,可以适应形参位置发生变化
    param_argument_dict = dict(zip(param_list, argument_list))

    # 拷贝一份函数节点的返回值子节点
    return_node = copy.deepcopy(function_node['body']['body'][0])
    if return_node['type'] != 'ReturnStatement':
        print(f'意料之外的函数节点,拥有超过一行的函数体: {function_node}')
        sys.exit()

    # 使用实参替换返回值节点中的形参,然后用返回值节点,替换掉整个函数调用node节点
    if return_node['argument']['type'] == 'Literal' or return_node['argument']['type'] == 'MemberExpression':
        # 直接替换
        node.clear()
        node.update(return_node['argument'])
    elif return_node['argument']['type'] == 'BinaryExpression' or return_node['argument']['type'] \
            == 'LogicalExpression':
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
    else:
        print(f'意料之外的函数返回值类型: {return_node}')
        sys.exit()
    # 替换完成后,将自身继续递归
    obj_property_reload(node)

    return


if __name__ == '__main__':
    with open('mid3.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    get_property_dict(data)
    with open('mid4.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs mid4.json mid4.js')
    # 验证对象名称是否有重复,如果有,就只能将JS分成单个部分传入还原
    # print(len(obj_property_dict))
    # print(len(obj_name_list))
    obj_property_reload(data)
    with open('mid5.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs mid5.json mid5.js')
