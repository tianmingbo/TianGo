function print_arg(addr){
    var module = Process.findRangeByAddress(addr);
    if(module != null) return hexdump(addr) + "\n";
    return ptr(addr) + "\n";
}
function hook_native_addr(funcPtr, paramsNum){
    var module = Process.findModuleByAddress(funcPtr);
    Interceptor.attach(funcPtr, {
        onEnter: function(args){
            this.logs = [];
            this.params = [];
            this.logs.push("call " + module.name + "!" + ptr(funcPtr).sub(module.base) + "\n");
            for(let i = 0; i < paramsNum; i++){
                this.params.push(args[i]);
                this.logs.push("this.args" + i + " onEnter: " + print_arg(args[i]));
            }
        }, onLeave: function(retval){
            for(let i = 0; i < paramsNum; i++){
                this.logs.push("this.args" + i + " onLeave: " + print_arg(this.params[i]));
            }
            this.logs.push("retval onLeave: " + print_arg(retval) + "\n");
            console.log(this.logs);
        }
    });
}

Java.perform(function () {
   var AuthorizeHelper = Java.use("com.mfw.tnative.AuthorizeHelper");
    AuthorizeHelper.xAuthencode.implementation = function (a, b, c, d, e) {
       //console.log("AuthorizeHelper.xAuthencode:", b, "||", c, "||", d, "||", e);
       var retval = this.xAuthencode(a, b, c, d, e);
       console.log(retval);
       return retval;
   }
});

function call_java(){
    Java.perform(function () {
        var AuthorizeHelper = Java.use("com.mfw.tnative.AuthorizeHelper");
        var data = "PUT&https%3A%2F%2Fmapi.mafengwo.cn%2Frest%2Fapp%2Fuser%2Flogin%2F&after_style%3Ddefault%26app_code%3Dcom.mfw.roadbook%26app_ver%3D8.1.6%26app_version_code%3D535%26brand%3Dgoogle%26channel_id%3DGROWTH-WAP-LC-3%26device_id%3DAC%253A37%253A43%253AA9%253A3F%253A34%26device_type%3Dandroid%26hardware_model%3DPixel%26mfwsdk_ver%3D20140507%26oauth_consumer_key%3D5%26oauth_nonce%3Dcfa857ff-8f4c-4268-8c75-37f07c7aaccf%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1632795895%26oauth_version%3D1.0%26open_udid%3DAC%253A37%253A43%253AA9%253A3F%253A34%26put_style%3Ddefault%26screen_height%3D1794%26screen_scale%3D2.625%26screen_width%3D1080%26sys_ver%3D10%26time_offset%3D480%26x_auth_mode%3Dclient_auth%26x_auth_password%3Da12345678%26x_auth_username%3D15968079477";
        var current_application = Java.use('android.app.ActivityThread').currentApplication();
        var context = current_application.getApplicationContext();
        AuthorizeHelper.$new("com.mfw.roadbook").xAuthencode(context, data, "", "com.mfw.roadbook", true);
    });
}

// var soAddr = Module.findBaseAddress("libmfw.so");
// var base64_encode = soAddr.add(0x6E3C + 1);
// hook_native_addr(base64_encode, 3);
//
// var Update = soAddr.add(0x6914 + 1);
// //hook_native_addr(Update, 3);
// Interceptor.attach(Update, {
//    onEnter: function (args) {
//        console.log(args[1].readCString());
//    }, onLeave: function (retval) {
//
//     }
// });
//
// var Final = soAddr.add(0x6A80 + 1);
// hook_native_addr(Final, 3);
//
// var SetKey = soAddr.add(0x6938 + 1);
// hook_native_addr(SetKey, 3);


