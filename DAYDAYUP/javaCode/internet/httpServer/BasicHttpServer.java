package internet.httpServer;

import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.*;

/**
 * @author tianmingbo
 */
public class BasicHttpServer {
    // 创建一个单线程执行器，用于启动 HTTP 服务器
    private static final ExecutorService BOOTSTRAP_EXECUTOR = Executors.newSingleThreadExecutor();
    // 创建一个线程池，用于处理来自客户端的 HTTP 请求
    private static ExecutorService taskExecutor;
    // 设置服务器监听的端口号
    private static final int PORT = 8999;

    // 启动 HTTP 服务器的方法
    static void startHttpServer() {
        // 获取处理器可用核心数，用于设置线程池大小
        int nThreads = Runtime.getRuntime().availableProcessors();
        System.out.println(nThreads);
        // 初始化线程池，设置线程池大小，队列大小和丢弃策略
        taskExecutor = new ThreadPoolExecutor(nThreads, nThreads, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue<>(100),
                new ThreadPoolExecutor.DiscardPolicy());
        System.out.println("start server success!!! port is " + PORT + ", and server is " + "127.0.0.1");
        // 循环尝试启动服务器，如果启动失败，则等待10秒后重试
        while (true) {
            try {
                ServerSocket serverSocket = new ServerSocket(PORT);
                BOOTSTRAP_EXECUTOR.submit(new ServerThread(serverSocket));
                break;
            } catch (Exception e) {
                try {
                    // 重试，等待 10 秒
                    TimeUnit.SECONDS.sleep(10);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            }
        }

        // 关闭启动执行器
        BOOTSTRAP_EXECUTOR.shutdown();
    }

    // HTTP 服务器主要任务类
    private static class ServerThread implements Runnable {
        // 保存传递给构造函数的 ServerSocket 实例
        private final ServerSocket serverSocket;

        // 构造函数
        public ServerThread(ServerSocket s) {
            this.serverSocket = s;
        }

        // 任务主体方法
        @Override
        public void run() {
            while (true) {
                try {
                    // 等待客户端连接
                    Socket socket = this.serverSocket.accept();
                    // 创建一个 HttpTask 实例，将 Socket 实例作为参数传递
                    HttpTask eventTask = new HttpTask(socket);
                    // 将 HttpTask 提交给 taskExecutor 执行
                    taskExecutor.submit(eventTask);
                } catch (Exception e) {
                    e.printStackTrace();
                    try {
                        // 如果发生异常，等待 1 秒后继续尝试
                        TimeUnit.SECONDS.sleep(1);
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
        }
    }

    public static void main(String[] args) {
        BasicHttpServer.startHttpServer();
    }
}
