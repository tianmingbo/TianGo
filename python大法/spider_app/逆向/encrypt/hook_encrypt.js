Java.perform(function () {
    function showStacks() {
        console.log(Java.use("android.util.log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
    }

    var ByteString = Java.use("com.android.okhttp.okio.ByteString");

    function toBase64(tag, data) {
        console.log(tag + "Base64: " + ByteString.of(data).base64());
    }

    function toHex(tag, data) {
        console.log(tag + "Hex: " + ByteString.of(data).hex());
    }

    function toUtf8(tag, data) {
        console.log(tag + "Utf8: " + ByteString.of(data).utf8());
    }

    var messageDigest = Java.use("java.security.MessageDigest");
    messageDigest.update.overload('byte').implementation = function (data) {
        console.log('messageDigest.update.(byte) is called')
        showStacks();
        return this.update(data);
    }

    messageDigest.update.overload('[B', 'int', 'int').implementation = function (data, start, length) {
        console.log("messageDigest.update.('[B', 'int', 'int') is called")
        showStacks();
        var algorithm = this.getAlgorithm(); //获取算法名：MD5，SHA
        var tag = algorithm + " update data";
        toBase64(tag, data);
        toUtf8(tag, data);
        toHex(tag, data);
        console.log("=========================================================================", start, length)
        return this.update(data, start, length);
    }

    messageDigest.update.overload('[B').implementation = function (data) {
        console.log("messageDigest.update.('[B') is called")
        showStacks();
        var algorithm = this.getAlgorithm(); //获取算法名：MD5，SHA
        var tag = algorithm + " update data";
        toBase64(tag, data);
        toUtf8(tag, data);
        toHex(tag, data);
        console.log("=========================================================================")
        return this.update(data);
    }

    messageDigest.digest.overload('[B').implementation = function (data) {
        console.log("messageDigest.digest.('[B') is called")
        showStacks();
        var algorithm = this.getAlgorithm();
        var res = this.digest(data);
        var tag = algorithm + " digest res";
        toBase64(tag, res);
        toUtf8(tag, res);
        toHex(tag, res);
        console.log("=========================================================================")
        return res;
    }

    //mac
    var mac = Java.use("javax.crypto.Mac");

    mac.init.overload("java.security.Key", "java.security.spec.AlgorithmParameterSpec").implementation = function (key, AlgorithmParameterSpec) {
        console.log("mac.init(key,AlgorithmParameterSpec) is called");
        return this.init(key, AlgorithmParameterSpec);
    }

    mac.init.overload("java.security.Key").implementation = function (key) {
        console.log("mac.init(key) is called");
        var algorithm = this.getAlgorithm(); //获取加密名
        var tag = algorithm + " init key";
        var keyByte = key.getEncoded(); //获取原来的byte数组
        toUtf8(tag, keyByte);
        toHex(tag, keyByte);
        toBase64(tag, keyByte);
        console.log("=====================================");
        return this.init(key);
    }
})