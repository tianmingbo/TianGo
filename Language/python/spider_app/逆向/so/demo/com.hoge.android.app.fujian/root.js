Java.perform(function () {
    function showStacks() {
        //$new() 实例化一个对象
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use('java.lang.Throwable').$new()))
    }

    //get stack at com.hoge.android.factory.welcome.WelcomeActivity$2$1.run(WelcomeActivity.java:260)
    var toast = Java.use("android.widget.Toast");
    toast.show.implementation = function () {
        console.log('toast show:');
        showStacks();
        return this.show();
    }

    var systemUtil = Java.use('com.hoge.android.factory.util.system.SystemUtils');
    systemUtil.checkSuFile.implementation = function () {
        return false;
    }
    systemUtil.checkRootFile.implementation = function () {
        return null;
    }


    //以下是hook检测root的部分实现
    Java.use("java.io.File").$init.overload("java.lang.String").implementation = function (str) {
        if (str.toLowerCase().endsWith("/su") || str.toLowerCase() == "su") {
            console.log("发现检测su文件");
            showStacks();
        }
        return this.$init(str);
    }
    Java.use("java.lang.Runtime").exec.overload("java.lang.String").implementation = function (str) {
        if (str.endsWith("/su") || str == "su") {
            console.log("发现尝试执行su命令的行为");
            showStacks();
        }
        return this.exec(str);
    }
    Java.use("java.lang.Runtime").exec.overload("[Ljava.lang.String;").implementation = function (stringArray) {
        for (var i = 0; i < stringArray.length; i++) {
            if (stringArray[i].includes("su") || stringArray[i].includes("/su") || stringArray[i] == "su") {
                console.log("发现尝试执行su命令的行为");
                showStacks();
                break;
            }
        }
        return this.exec(stringArray);
    }
    Java.use("java.lang.ProcessBuilder").$init.overload("[Ljava.lang.String;").implementation = function (stringArray) {
        for (var i = 0; i < stringArray.length; i++) {
            if (stringArray[i].includes("su") || stringArray[i].includes("/su") || stringArray[i] == "su") {
                console.log("发现尝试执行su命令的行为");
                showStacks();
                break;
            }
        }
        return this.$init(stringArray);
    }
})


//frida -U -f com.hoge.android.app.fujian -l .\root.js --no-pause