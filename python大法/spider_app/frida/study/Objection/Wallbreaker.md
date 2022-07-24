## WTF?

一个objection插件，可以通过类实例打印出相应类的具体内容，包括静态成员和实例成员的值以及类中的所有函数。

## commands

- objection -N -h 192.168.1.3 -p 8888  -g com.hello.qqc   explore -P  C:\Users\kkk\.objection\plugins   设置端口及添加插件（首先需要下载插件Wallbreaker）
- plugin wallbreaker objectsearch android.app.AlertDialog 搜索类实例，会输入实例的内存地址
- plugin wallbreaker objectdump 0x2582 把实例的内容打印出来