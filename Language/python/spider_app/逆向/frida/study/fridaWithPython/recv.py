# -*- coding: UTF-8 -*-
import frida, sys
import time

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
            console.log('MD5 string: ', a);
            var retval = this.md5(a);
            send(retval);
            //接收来自Python的数据
            recv(function(obj){
                console.log(JSON.stringify(obj));
                console.log("Python:", obj.data);
                retval = obj.data;
            }).wait(); //等待
            return retval;
        }
    });
"""


def messageFunc(message, data):
    print(message)
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
        time.sleep(5)
        script.post({"data": message['payload']})  # 发送数据给js
    else:
        print(message)


# get_usb_device
# get_remote_device
process = frida.get_usb_device().attach('com.dodonew.online')
script = process.create_script(jsCode)
script.on('message', messageFunc)
script.load()
print("开始运行")
sys.stdin.read()
