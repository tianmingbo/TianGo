# @Time : 2022/4/17 13:03
# @Author :bo~
# @FileName: hook_native.py
# @Description: hook native文件
import frida
import sys

CODE = open('hook_native.js', encoding='utf-8').read()
PROCESS_NAME = 'AppBasic2'


def on_message(message, data):
    print(message)


process = frida.get_remote_device().attach(PROCESS_NAME)  # 获取连接设备并挂载进程
script = process.create_script(CODE)  # 往进程中注入Hook脚本
script.on('message', on_message)  # 监听message事件，回调方法是on_message，任何通过js send方法发送的数据，on_message都能收到
script.load()  # 注入脚本
sys.stdin.read()
