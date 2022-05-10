from os.path import realpath, dirname, join
import json


def get_config(name):
    # 读取配置文件
    path = join(dirname(realpath(__file__)), 'configs', f'{name}.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())
