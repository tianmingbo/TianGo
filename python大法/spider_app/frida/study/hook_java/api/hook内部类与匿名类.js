Java.perform(function () {
    //内部类hook：类层级$内部类名
    Java.choose("com.xjb.hook.Wallet$InnerStructure", {
        onMatch: function (obj) {
            console.log("内部类", obj.backCardList.value)
        }, onComplete: function () {
        }
    });
    //$1是在该类中的第几个匿名类
    var money$1 = Java.use('com.xjb.app.MainActivity$1');
    money$1.getInfo.implementation = function () {
        var res = this.getInfo();
        console.log("匿名类",res)
        return res;
    }
})