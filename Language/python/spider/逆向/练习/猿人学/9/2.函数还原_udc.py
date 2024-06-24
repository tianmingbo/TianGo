import json
import os

import execjs


def call_function_reload(node, ctx):
    # 从根遍历节点
    try:
        if type(node) == list:
            for item in node:
                call_function_reload(item, ctx)
            return
        elif type(node) != dict:
            return
    except Exception as e:
        print(f'error->{e}')
    # 捕获一个 CallExpression 节点
    try:
        if node['type'] == 'CallExpression':
            if node['callee']['name'] == '_0x56ae':
                arg_list = []
                for item in node['arguments']:
                    if item['type'] != 'Literal':
                        break
                    arg_list.append(item['value'])  # 提取参数
                value = ctx.call('_0x56ae', *arg_list)
                print(value)
                new_node = {'type': 'Literal', 'value': value}
                node.clear()
                node.update(new_node)
                return
    except Exception:
        pass
    for key in node.keys():
        call_function_reload(node[key], ctx)


if __name__ == '__main__':
    # 可先还原大数组，提升替换速度
    with open('udc.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    with open('udc_array_reload.js', 'r', encoding='utf-8') as f:
        ctx = execjs.compile(f.read())
    call_function_reload(data, ctx)
    with open('udc_mid1.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('node JsonToJs udc_mid1.json udc_mid1.js')
