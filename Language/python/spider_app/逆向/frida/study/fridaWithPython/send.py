# -*- coding: UTF-8 -*-
import frida, sys

jsCode = """
    Java.perform(function(){
        var RequestUtil = Java.use('com.dodonew.online.http.RequestUtil');
        RequestUtil.encodeDesMap.overload('java.lang.String', 'java.lang.String', 'java.lang.String').implementation = function(a, b, c){
            console.log('data: ', a);
            console.log('desKey: ', b);
            console.log('desIV: ', c);
            var retval = this.encodeDesMap(a, b, c);
            console.log('retval: ', retval);
            return retval;
        }
        var Utils = Java.use('com.dodonew.online.util.Utils');
        Utils.md5.implementation = function(a){
            var retval = this.md5(a);
            send(retval); //发送给python
            console.log('retval: ', retval);
            return retval;
        }
    });
"""


def messageFunc(message, data):
    print(message)
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
    else:
        print(message)


# get_usb_device
# get_remote_device
process = frida.get_usb_device().attach('com.dodonew.online')
script = process.create_script(jsCode)
script.on('message', messageFunc)  # 注册事件
script.load()
print("开始运行")
sys.stdin.read()
