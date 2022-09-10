# @Time : 2022/4/15 21:53
# @Author :bo~
# @FileName: hook_java.py
# @Description: frida hook java
import frida
import sys

CODE = open('hook_java.js', encoding='utf-8').read()
PROCESS_NAME = 'AppBasic1'


def on_message(message, data):
    print(message)


"""
手机需要安装frida-server，修改777权限。修改端口转发。
url：https://www.jianshu.com/p/22ced178b29c
"""
process = frida.get_remote_device().attach(PROCESS_NAME)  # 获取连接设备并挂载进程
script = process.create_script(CODE)  # 往进程中注入Hook脚本
script.on('message', on_message)  # 监听message事件，回调方法是on_message，任何通过js send方法发送的数据，on_message都能收到
script.load()  # 注入脚本
sys.stdin.read()
