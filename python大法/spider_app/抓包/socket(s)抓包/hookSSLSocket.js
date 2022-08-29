Java.perform(function () {
    Java.use('com.android.org.conscrypt.ConscryptFileDescriptorSocket$SSLOutputStream').write.overload('[B', 'int', 'int').implementation = function (byteArray, int1, int2) {
        var res = this.write(byteArray, int1, int2);
        console.log('write res,byteArray,int1,int2=>', res, byteArray, int1, int2);
        // var ByteString = Java.use.md('com.android.okhttp.okio.ByteString');
        // console.log('contents:=>', ByteString.of(b).hex());
        jhexdump(byteArray)
        return res;
    }

    function jhexdump(array) {
        //byte数组可视化
        var ptr = Memory.alloc(array.length); //开辟内存
        for (var i = 0; i < array.length; ++i)
            Memory.writeS8(ptr.add(i), array[i]) //存入手动开辟的内存
        console.log(hexdump(ptr, {offset: 0, length: array.length, header: false, ansi: false}));
    }

    Java.use('com.android.org.conscrypt.ConscryptFileDescriptorSocket$SSLInputStream').read.overload('[B', 'int', 'int').implementation = function (byteArray, int1, int2) {
        var res = this.read(byteArray, int1, int2);
        console.log('read res,byteArray,int1,int2=>', res, byteArray, int1, int2);
        // var ByteString = Java.use.md('com.android.okhttp.okio.ByteString');
        // console.log('contents:=>', ByteString.of(b).hex());
        jhexdump(byteArray)
        return res;
    }
})