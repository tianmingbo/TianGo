import json
import os


def concat_obj_property_name(node):
    if type(node) == list:
        for item in node:
            concat_obj_property_name(item)
        return
    elif type(node) != dict:
        return
    # 捕获一个二元运算节点
    if 'type' in node and node['type'] == 'BinaryExpression':
        if not (node['left']['type'] == 'Literal' and node['right']['type'] == 'Literal'):
            concat_obj_property_name(node['left'])
            concat_obj_property_name(node['right'])
        if node['left']['type'] == 'Literal' and node['right']['type'] == 'Literal':
            # 构造新节点
            new_node = {'type': 'Literal', 'value': node['left']['value'] + node['right']['value']}
            node.clear()
            node.update(new_node)
            return
    for key in node.keys():
        concat_obj_property_name(node[key])


if __name__ == '__main__':
    with open('mz2.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    concat_obj_property_name(data)
    with open('mz3.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('/usr/local/bin/node JsonToJs mz3.json mz3.js')
