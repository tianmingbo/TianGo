# @Time : 2022/6/27 23:05
# @Author :bo~
# @FileName: loader.py
# @Description: rpc调用

import frida


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


with open('call.js', encoding='utf-8') as f:
    js_code = f.read()
device = frida.get_usb_device(timeout=1000)  # 获取usb设备,设置超时时间1s
process = device.attach('junior')  # 注入

script = process.create_script(js_code)  # 加载js代码

script.on('message', on_message)  # 注册自己的消息对应的函数
script.load()
for i in range(20, 30):
    for j in range(1, 10):
        script.exports.sub(str(i), str(j))
