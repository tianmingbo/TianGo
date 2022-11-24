const AnyProxy = require("anyproxy");

const options = {
    port: 10086,
    rule: require("./rules"),
    webInterface: {
        enable: true,
        webPort: 8002
    },
    throttle: 10000,
    forceProxyHttps: true,
    wsIntercept: false, // 不开启websocket代理
    silent: false
};
//开启全局代理
AnyProxy.utils.systemProxyMgr.enableGlobalProxy('127.0.0.1', options.port)
const proxyServer = new AnyProxy.ProxyServer(options);

proxyServer.on("ready", () => { /* */
});
proxyServer.on("error", (e) => { /* */
});
proxyServer.start();