1、输出内存中所有类
2、在日志中过滤HTTPURLConnection和okhttp(3)的相关类
3、补全android hooking watch class **类，监控内存中所有和发包相关的类 (-c filename)
4、手动触发操作，看是否有方法被调用。然后退出重新注入，hook对应方法。
5、如果对类有混淆，https://github.com/siyujie/okhttpLogger-Frida 解决