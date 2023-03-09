package internet.d10_bs;

import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.*;

/**
    了解：BS-浏览器-服务器基本了解。

    引入：
        之前客户端和服务端都需要自己开发。也就是CS架构。
        接下来模拟一下BS架构。

    客户端：浏览器。（无需开发）
    服务端：自己开发。
    需求：在浏览器中请求本程序，响应一个网页文字给浏览器显示


 */
public class BSserverDemo {
    // 使用静态变量记住一个线程池对象
    private static ExecutorService pool = new ThreadPoolExecutor(3,
            5, 6, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(2)
            , Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());

    public static void main(String[] args) {
        try {
            // 1.注册端口
            ServerSocket ss = new ServerSocket(8080);
            // 2.创建一个循环接收多个客户端的请求。
            while(true){
                Socket socket = ss.accept();
                // 3.交给一个独立的线程来处理！
                pool.execute(new ServerReaderRunnable(socket));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

