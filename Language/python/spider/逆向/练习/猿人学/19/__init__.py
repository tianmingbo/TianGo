"""
ja3指纹检测

客户端发起https的请求第一步是向服务器发送tls握手请求，其中就包含了客户端的一些特征
相关内容在tls协议报文中Client Hello的Transport Layer Security当中

ja3指纹=SSLVersion(协议版本)+Cipher(密码套件)+SSLExtension(ssl扩展类型)+EllipticCurve（Extension: supported_groups ）+EllipticCurvePointFormat（Elliptic curves point formats ），requests的Elliptic curves point formats是0,1,2，chrome的是0

https://www.cnblogs.com/ospider/p/python-curl-cffi-tls-fingerprint.html
https://ares-x.com/2021/04/18/SSL-%E6%8C%87%E7%BA%B9%E8%AF%86%E5%88%AB%E5%92%8C%E7%BB%95%E8%BF%87
"""
