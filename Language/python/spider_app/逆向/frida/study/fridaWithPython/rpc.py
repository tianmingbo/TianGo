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
            console.log('retval: ', retval);
            return retval;
        }
    });
    
    function test(data){
        var result = "";
        Java.perform(function(){
            result = Java.use('com.dodonew.online.util.Utils').md5(data);
        });
        return result;
    }
    //导出接口
    rpc.exports = {
        rpcfunc: test
    };
    
"""

# get_usb_device
# get_remote_device
device = frida.get_usb_device()
pid = device.spawn(["com.dodonew.online"])  # 以挂起方式创建进程
process = device.attach(pid)
script = process.create_script(jsCode)
script.load()
device.resume(pid)  # 加载完脚本, 恢复进程运行

# 调用rpc
for _ in range(10000):
    result = script.exports.rpcFUnc('dali666')  # 调用rpc，rpcFUnc函数名默认小写
    print(result)
print("开始运行")
sys.stdin.read()
