## 过root检测 & 过抓包检测
### step

1. hook Toast.show()方法，根据堆栈，找到方法com.hoge.android.factory.welcome.WelcomeActivity$2$1.run(WelcomeActivity.java:260)
2. 注意二级指针，需要再readPointer()，取值