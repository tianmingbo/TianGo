# -*- coding: UTF-8 -*-
import frida
import sys

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
            console.log('retval: ', retval);
            return retval;
        }
    });
"""

device = frida.get_usb_device(timeout=1000)
print("device: ", device)
pid = device.spawn(["com.dodonew.online"])  # 以挂起方式创建进程
print("pid: ", pid)
process = device.attach(pid)
print("process: ", process)
script = process.create_script(jsCode)
script.load()
device.resume(pid)  # 加载完脚本, 恢复进程运行
print("开始运行")
sys.stdin.read()  # 阻塞控制台
