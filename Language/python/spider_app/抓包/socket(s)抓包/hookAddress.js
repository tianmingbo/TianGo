function hookAddress() {
    Java.perform(function () {
        Java.use('java.net.InetSocketAddress').$init.overload('java.net.InetAddress', 'int').implementation = function (addr, port) {
            var res = this.$init(addr, port);
            if (addr.isSiteLocalAddress()) {
                console.log('Local address=>', addr.toString(), ', port is ', port)
            } else {
                console.log('Server address=>', addr.toString(), ', port is ', port)
            }
            return res;
        }
    })
}