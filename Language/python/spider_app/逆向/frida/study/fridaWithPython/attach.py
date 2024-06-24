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
            console.log('MD5 string: ', a);
            var retval = this.md5(a);
            console.log(retval);
            return retval;
        }
    });
"""

# get_usb_device
# get_remote_device
# process = frida.get_usb_device(timeout=1000).attach('com.dodonew.online')  # 通过包名注入
# process = frida.get_usb_device(timeout=1000).attach(26702)  # pid注入
process = frida.get_device_manager().add_remote_device('127.0.0.1:27042').attach('com.dodonew.online')
script = process.create_script(jsCode)
script.load()
print("开始运行")
sys.stdin.read()
