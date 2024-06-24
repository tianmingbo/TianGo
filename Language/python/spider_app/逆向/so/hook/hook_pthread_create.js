function hook_pthread_create() {
    var pthread_create_addr = Module.findExportByName("libc.so", "pthread_create");
    console.log("pthread_create_addr: ", pthread_create_addr);
    Interceptor.attach(pthread_create_addr, {
        onEnter: function (args) {
            console.log(args[0], args[1], args[2], args[4]);
        }, onLeave: function (retval) {
            console.log("retval is =>", retval)
        }
    })
}

hook_pthread_create();