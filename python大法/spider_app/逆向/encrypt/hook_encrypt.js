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

    mac.doFinal.overload().implementation = function () {
        console.log("mac.doFinal() is called");
        var res = this.doFinal();
        var algorithm = this.getAlgorithm(); //获取加密名
        var tag = algorithm + " doFinal key";
        toUtf8(tag, res);
        toHex(tag, res);
        toBase64(tag, res);
        console.log("=====================================");
        return res;
    }

    mac.doFinal.overload('[B').implementation = function (data) {
        console.log("mac.doFinal('[B') is called");
        return this.doFinal(data);
    }

    mac.doFinal.overload('[B', 'int').implementation = function (data, outOffset) {
        console.log("mac.doFinal('[B', 'int') is called");
        return this.doFinal(data, outOffset);
    }

    //AES DES hook, hook init 可以得到iv，密钥
    var cipher = Java.use("javax.crypto.Cipher");


    cipher.init.overload("int", "java.security.cert.Certificate").implementation = function () {
        console.log('Cipher.init("int", "java.security.cert.Certificate") is called');
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.init.overload("int", "java.security.cert.Certificate", "java.security.SecureRandom").implementation = function () {
        console.log('Cipher.init("int", "java.security.cert.Certificate", "java.security.SecureRandom") is called');
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.init.overload("int", "java.security.Key", "java.security.SecureRandom").implementation = function () {
        console.log('Cipher.init("int", "java.security.Key","java.security.SecureRandom") is called');
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.init.overload("int", "java.security.Key", "java.security.spec.AlgorithmParameterSpec", "java.security.SecureRandom").implementation = function () {
        console.log('Cipher.init("int", "java.security.Key",,"java.security.spec.AlgorithmParameterSpec","java.security.SecureRandom") is called');
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.init.overload("int", "java.security.Key", "java.security.AlgorithmParameters", "java.security.SecureRandom").implementation = function () {
        console.log('Cipher.init("int", "java.security.Key","java.security.AlgorithmParameters","java.security.SecureRandom") is called');
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.init.overload("int", "java.security.Key").implementation = function () {
        console.log('Cipher.init("int", "java.security.Key") is called');
        showStacks()
        var algorithm = this.getAlgorithm();
        var tag = algorithm + " init key";
        var keyBytes = arguments[1].getEncoded(); //获取密钥字节
        toBase64(tag, keyBytes);
        toHex(tag, keyBytes);
        toUtf8(tag, keyBytes);
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.init.overload("int", "java.security.Key", "java.security.spec.AlgorithmParameterSpec",).implementation = function () {
        console.log('Cipher.init("int", "java.security.Key","java.security.spec.AlgorithmParameterSpec") is called');
        showStacks();
        var algorithm = this.getAlgorithm();
        var tag = algorithm + " init key";
        var keyBytes = arguments[1].getEncoded(); //获取密钥字节
        toBase64(tag, keyBytes);
        toHex(tag, keyBytes);
        toUtf8(tag, keyBytes);
        var tags = algorithm + " init iv"
        var iv = Java.cast(arguments[2], Java.use("javax.crypto.spec.IvParameterSpec"));//向下转型，因为接收的是AlgorithmParameterSpec类
        var ivByte = iv.getIV(); //获取iv byte
        toUtf8(tags, ivByte);
        toBase64(tags, ivByte);
        toHex(tags, ivByte);
        console.log('==================================================================')
        return this.init.apply(this, arguments);
    }

    cipher.doFinal.overload().implementation = function () {
        console.log('Cipher.doFinal() is called');
        console.log('==================================================================')
        return this.doFinal.apply(this, arguments);
    }

    cipher.doFinal.overload("[B").implementation = function () {
        console.log('Cipher.doFinal("[B") is called');
        showStacks();
        var algorithm = this.getAlgorithm();
        var tag = algorithm + " doFinal data";
        var data = arguments[0];
        toHex(tag, data);
        toBase64(tag, data);
        toUtf8(tag, data);
        var res = this.doFinal.apply(this, arguments);
        var tags = algorithm + "doFinal res"
        toHex(tags, res);
        toBase64(tags, res);
        toUtf8(tags, res);
        console.log('==================================================================')
        return res;
    }

    cipher.doFinal.overload("[B", "int").implementation = function () {
        console.log('Cipher.doFinal("[B", "int") is called');
        console.log('==================================================================')
        return this.doFinal.apply(this, arguments);
    }

    cipher.doFinal.overload("[B", "int", "int").implementation = function () {
        showStacks();
        var algorithm = this.getAlgorithm();
        var tag = algorithm + " doFinal data";
        var data = arguments[0]; //加密的明文
        toHex(tag, data);
        toBase64(tag, data);
        toUtf8(tag, data);
        var res = this.doFinal.apply(this, arguments); //结果
        var tags = algorithm + "doFinal res"
        toHex(tags, res);
        toBase64(tags, res);
        toUtf8(tags, res);
        console.log('==================================================================', arguments[1], arguments[2])
        return res;
    }

    cipher.doFinal.overload("[B", "int", "int", "[B").implementation = function () {
        console.log('Cipher.doFinal("[B", "int", "int", "[B") is called');
        console.log('==================================================================')
        return this.doFinal.apply(this, arguments);
    }

    cipher.doFinal.overload("[B", "int", "int", "[B", "int").implementation = function () {
        console.log('Cipher.doFinal("[B", "int", "int", "[B", "int") is called');
        console.log('==================================================================')
        return this.doFinal.apply(this, arguments);
    }

    cipher.doFinal.overload("java.nio.ByteBuffer", "java.nio.ByteBuffer").implementation = function () {
        console.log('Cipher.doFinal("java.nio.ByteBuffer", "java.nio.ByteBuffer") is called');
        console.log('==================================================================')
        return this.doFinal.apply(this, arguments);
    }
})