1. objection -g com.android.settiings explore 注入’设置‘应用，注入成功就会进入命令界面
2. android hooking list classes 列出内存中的所有类
3. android hooking search classes  className 在内存已加载的类中搜索包含特定关键词的类
4. android hooking search methods \<key> 搜索所有包含关键词key的方法
5. android hooking list class_methods \<class_name> 列出类class_name的所有方法
6. android hooking list activities 列出进程的所有活动activity
7. android hooking list services 列出进程的所有service
8. android hooking watch class_method \<methodName> 对指定的方法进行hook。例：android hooking watch class_method java.io.File.$init --dump-args --dump-backtrace --dump-return  三个参数分别是：打印函数的参数、调用栈和返回值
9. jobs kill \<id> 删除作业，删除上一条加入的job
10. android hooking watch class \<classname> hook类中的所有函数，（不包括构造函数）
11. android heap search instances \<classname> 搜索类实例
12. android heap execute \<HashCode> \<methodname> 执行实例方法
13. android heap evaluate \<HashCode> 执行带参数的函数，需要先执行这个，然后在编译器中输入脚本
14. android intent launch_activity com.example.junior.CalculatorActivity 启动活动
15. ./frida-server-15.1.17-android-arm64  -l 0.0.0.0:8888 设置服务端口
16. objection -g com.hello.qqc explore -s "android hooking watch class android.App.AlertDialog"  在app启动的时候hook
