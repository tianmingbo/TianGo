1. 抓包工具抓包--charles|httpcanary
2. jdax解包,发现加固.使用自定义安卓系统打印出dex
3. java层hook，hook算法。
4. 登录界面hook getByte方法，定位到getSign方法，发现是native方法
5. IDA反编译so，定位到java_com_sichuanol_cbgc_util_SignManager_getSign方法
6. 定位到关键方法get32MD5String()地址0x8BC，so层hook