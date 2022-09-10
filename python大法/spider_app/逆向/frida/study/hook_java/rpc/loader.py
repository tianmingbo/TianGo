# @Time : 2022/6/27 23:05
# @Author :bo~
# @FileName: loader.py
# @Description: rpc调用

import sys, frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


with open('hook.js', encoding='utf-8') as f:
    js_code = f.read()
device = frida.get_usb_device(timeout=1000)  # 获取usb设备,设置超时时间1s
process = device.attach('demo02')  # 注入

script = process.create_script(js_code)  # 加载js代码

script.on('message', on_message)  # 注册自己的消息对应的函数
script.load()

command = ""
while True:
    command = input("\nEnter command:\n1:Exit\n2:Call secret function\n3:get total Value\nchoice")
    if command == '1':
        break
    elif command == '2':
        script.exports.callsecertfunc()  # 访问js中定义的导出名
    elif command == '3':
        script.exports.gettotalvalue()
