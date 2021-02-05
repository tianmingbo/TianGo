# ZMQ

<u></u>

zmq有三种模式：

### **①Request---Reply模式：客户端在请求后，服务端必须响应**

![image-20200828114521310](C:\Users\mingb\AppData\Roaming\Typora\typora-user-images\image-20200828114521310.png)

### **②Publish--Subscribe模式：广播所有client，没有队列缓存，断开连接数据永远消失。client可以进行数据过滤**

![image-20200828135636663](C:\Users\mingb\AppData\Roaming\Typora\typora-user-images\image-20200828135636663.png)