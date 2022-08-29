Java.perform(function () {
    //hook请求
    Java.use('java.net.SocketOutputStream').socketWrite.overload('[B', 'int', 'int').implementation = function (b, off, len) {
        var res = this.socketWrite(b, off, len);
        console.log('socketWrite res,b,off,len=>', res, b, off);
        var ByteString = Java.use('com.android.okhttp.okio.ByteString');
        // console.log('contents:=>', ByteString.of(b).hex());
        jhexdump(b)
        return res;
    }

    function jhexdump(array) {
        var ptr = Memory.alloc(array.length); //开辟内存
        for (var i = 0; i < array.length; ++i)
            Memory.writeS8(ptr.add(i), array[i]) //存入手动开辟的内存
        console.log(hexdump(ptr, {offset: 0, length: array.length, header: false, ansi: false}));
    }

    //hook response
    Java.use('java.net.SocketInputStream').read.overload('[B', 'int', 'int').implementation = function (bytearray, int1, int2) {
        var res = this.read(bytearray, int1, int2);
        console.log('socketWrite res,bytearray,int1,int2=>', bytearray, int1, int2);
        var ByteString = Java.use('com.android.okhttp.okio.ByteString');
        // console.log('contents:=>', ByteString.of(b).hex());
        jhexdump(bytearray)
        return res;
    }
})