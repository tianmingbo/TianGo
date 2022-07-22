# @Time : 2022/6/27 23:05
# @Author :bo~
# @FileName: loader.py
# @Description: rpc调用


"""
frida逆向三板斧
1：Objection快速Hook定位，
2：通过frida脚本进行关键函数的逻辑修改与主动调用
3：frida脚本结合python对关键函数调用
"""
import frida


def on_message(message, data):
    if message['type'] == 'send':  # 接收js send发送的数据
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
