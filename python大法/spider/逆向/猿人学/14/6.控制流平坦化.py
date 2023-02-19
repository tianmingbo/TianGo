import json
import os


def sort_code(node):
    if type(node) == list:
        try:
            if len(node) == 2 and node[1]['type'] == 'WhileStatement' and node[0]['type'] == 'VariableDeclaration':
                for i in node[0]['declarations']:
                    if i['type'] == 'VariableDeclarator' and i['init'] and \
                            i['init']['type'] == 'CallExpression':
                        sort_list = i['init']['callee']['object']['value'].split('|')
                        cases_list = node[1]['body']['body'][0]['cases']
                        result_list = [cases_list[int(i)]['consequent'][0] for i in sort_list]
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
    with open('mz5.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    sort_code(data)
    with open('mz6.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))
    os.system('/usr/local/bin/node JsonToJs mz6.json mz6.js')
