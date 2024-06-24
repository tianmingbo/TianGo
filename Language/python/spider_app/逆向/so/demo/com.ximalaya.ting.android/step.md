## ollvm字符串混淆
```
使用jnitrace hook jni函数
https://github.com/chame1eon/jnitrace

command：jnitrace -m attach -l libencrypt.so com.ximalaya.ting.android 附加
```

## ollvm字符串解密
```
1 直接打印内存中的字符串，一般都是解密状态，缺点是一个个打印比较繁琐
2 使用jnitrace，缺点是只能查看jni相关函数
3 从内存中dump整个so，放到ida中逆向分析，缺点是需要修复,SoFixer（通用）
4 分析so中的字符串解密函数，然后还原
```